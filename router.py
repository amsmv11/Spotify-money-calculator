import base64
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from fastapi import APIRouter, Response
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse
from httpx import AsyncClient
from dotenv import load_dotenv

load_dotenv()


router = APIRouter()


class SpotifyAppCredentials(BaseSettings):
    client_id: str
    client_secret: str
    state: str
    scope: str
    redirect_url: str

    class Config:
        env_prefix = "SPOTIFY_"


class SpotifyUserCredentials(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str


@router.get("/")
async def root():
    return FileResponse("static/index.html")


@router.get("/login")
async def login():
    spotify_credentials = SpotifyAppCredentials()

    return RedirectResponse(
        f"https://accounts.spotify.com/authorize?"
        f"response_type=code&client_id={spotify_credentials.client_id}&"
        f"scope={spotify_credentials.scope}&redirect_uri={spotify_credentials.redirect_url}&"
        f"state={spotify_credentials.state}"
    )


@router.get("/callback")
async def callback(code: str, state: str):
    spotify_credentials = SpotifyAppCredentials()

    if state != spotify_credentials.state:
        return Response("State Mismatch", status_code=403)

    async with AsyncClient() as client:
        auth_string = (
            f"{spotify_credentials.client_id}:{spotify_credentials.client_secret}"
        )
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

        response = await client.post(
            url="https://accounts.spotify.com/api/token",
            headers={
                "Authorization": f"Basic {auth_base64}",
            },
            data={
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": spotify_credentials.redirect_url,
            },
        )

        try:
            response.raise_for_status()
        except BaseException as e:
            error_template_path = Path("static/error.html")
            error_html = error_template_path.read_text()

            error_html = error_html.replace("{status_code}", str(response.status_code))
            error_html = error_html.replace("{error_message}", str(e))

            return HTMLResponse(content=error_html, status_code=response.status_code)

        user_credentials = SpotifyUserCredentials(**response.json())

        return f"OAuth Flow completed successfuly {user_credentials}"
