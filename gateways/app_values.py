from decimal import Decimal
from typing import List, Literal
from pydantic import BaseModel


class AlbumsPriceRequestItem(BaseModel):
    artist: str
    album_name: str


class AlbumsPriceResponseItem(AlbumsPriceRequestItem):
    price: Decimal
    valid: bool  # Reflects if the api was able to find a price


class AlbumsPriceRequest(BaseModel):
    albums: List[AlbumsPriceRequestItem]


class AlbumsPriceResponse(BaseModel):
    albums_with_price: List[AlbumsPriceResponseItem]
    total: float
    currency: Literal["EUR"]
