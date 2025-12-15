from typing import List
import discogs_client
from fastapi import Request

from gateways.app_values import (
    AlbumsPriceRequest,
    AlbumsPriceResponse,
    AlbumsPriceResponseItem,
)
from services.cache import cache_response
from values.discogs_values import DiscogsPriceSuggestions, DiscogsSettings
from values.spotify_values import SpotifyAlbumListItem
from . import spotify_gateway


def create_discogs_client() -> discogs_client.Client:
    settings = DiscogsSettings()
    return discogs_client.Client(
        "SpotifyMoneyCalculator/1.0", user_token=settings.access_token
    )


client = create_discogs_client()


@cache_response(ttl=864000, namespace="albums")
async def get_price_of_album(artist: str, album_name: str):
    """
    This function returns the price of the album and a bool that reflects whether it was
    able to find the price for it or not

    :param albums_price_request_item: Description
    :type albums_price_request_item: AlbumsPriceRequestItem
    """

    results = client.search(
        f"{artist} - {album_name} CD",
        type="release",
    )

    if not results:
        return 0.0, False

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
    response = AlbumsPriceResponse(albums_with_price=[], currency="EUR", total=0.0)

    for album_request_item in albums_price_request.albums:
        album_price, was_price_found = await get_price_of_album(
            album_request_item.artist, album_request_item.album_name
        )
        response.albums_with_price.append(
            AlbumsPriceResponseItem(
                **album_request_item.__dict__, price=album_price, valid=was_price_found
            )
        )

        response.total += album_price

    return response


async def get_all_ambums_price(request: Request) -> AlbumsPriceResponse:
    response = AlbumsPriceResponse(albums_with_price=[], currency="EUR", total=0.0)

    all_albums_response: List[SpotifyAlbumListItem] = (
        await spotify_gateway.get_user_saved_albums(request=request, limit=-1) or []
    )

    for album_response in all_albums_response:
        artist = album_response.album.artists[0].name
        album_name = album_response.album.name

        album_price, was_price_found = await get_price_of_album(artist, album_name)
        response.albums_with_price.append(
            AlbumsPriceResponseItem(
                album_name=album_name,
                artist=artist,
                price=album_price,
                valid=was_price_found,
            )
        )

        response.total += album_price

    return response
