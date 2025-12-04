from fastapi import APIRouter
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from gateways import spotify_gateway

load_dotenv()

router = APIRouter()


@router.get("/")
async def root():
    return FileResponse("static/index.html")


@router.get("/login")
async def login():
    return spotify_gateway.login()


@router.get("/callback")
async def callback(code: str, state: str):
    return await spotify_gateway.callback(code=code, state=state)
