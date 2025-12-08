from decimal import Decimal
import discogs_client

from gateways.app_values import (
    AlbumsPriceRequest,
    AlbumsPriceRequestItem,
    AlbumsPriceResponse,
    AlbumsPriceResponseItem,
)
from services.cache import cache_response
from values.discogs_values import DiscogsPriceSuggestions, DiscogsSettings


def create_discogs_client() -> discogs_client.Client:
    settings = DiscogsSettings()
    return discogs_client.Client(
        "SpotifyMoneyCalculator/1.0", user_token=settings.access_token
    )


client = create_discogs_client()


@cache_response(ttl=864000, namespace="albums")
async def get_price_of_album(albums_price_request_item: AlbumsPriceRequestItem):
    """
    This function returns the price of the album and a bool that reflects whether it was
    able to find the price for it or not

    :param albums_price_request_item: Description
    :type albums_price_request_item: AlbumsPriceRequestItem
    """

    results = client.search(
        f"{albums_price_request_item.artist} - {albums_price_request_item.album_name} CD",
        type="release",
    )

    release = results[0]

    if not release:
        return 0.0, False

    response = client._request(
        "GET", f"https://api.discogs.com/marketplace/price_suggestions/{release.id}"
    )

    price_suggestions = DiscogsPriceSuggestions(**response)

    response = price_suggestions.return_price_based_on_quality_vs_price()

    return response, True if response else False


async def get_price_of_albums(
    albums_price_request: AlbumsPriceRequest,
) -> AlbumsPriceResponse:
    response = AlbumsPriceResponse(
        albums_with_price=[], currency="EUR", total=Decimal(0)
    )

    for album_request_item in albums_price_request.albums:
        album_price, was_price_found = await get_price_of_album(album_request_item)
        response.albums_with_price.append(
            AlbumsPriceResponseItem(
                **album_request_item.__dict__, price=album_price, valid=was_price_found
            )
        )

        response.total += album_price

    return response
