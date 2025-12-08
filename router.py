from fastapi import APIRouter, Request
from gateways import spotify_gateway
from gateways.app_values import AlbumsPriceRequest
from gateways.discogs_gateway import get_price_of_albums

router = APIRouter()


@router.get("/")
async def root(request: Request):
    return await spotify_gateway.root(request=request)


@router.get("/login")
async def login():
    return spotify_gateway.login()


@router.get("/callback")
async def callback(request: Request, code: str, state: str):
    return await spotify_gateway.callback(request=request, code=code, state=state)


@router.get("/user_albums")
async def user_albums(request: Request, limit: int):
    return await spotify_gateway.get_user_saved_albums(request=request, limit=limit)


@router.post("/get_albums_price")
async def get_albums_price(albums_price_request: AlbumsPriceRequest):
    return get_price_of_albums(albums_price_request)
