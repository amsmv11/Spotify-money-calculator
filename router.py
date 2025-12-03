import base64
from pydantic import BaseModel
from fastapi import APIRouter, Response
from fastapi.responses import RedirectResponse
from httpx import AsyncClient
from dotenv import load_dotenv

load_dotenv()


router = APIRouter()


class SpotifyAppCredentials(BaseModel):
    client_id: str = "bc41d365e31a491fa21d707e75072740"
    client_secret: str = "b68e5950da074f359ca1ca0b7ab57c36"
    state: str = "thisarandomstate"
    scope: str = "user-read-private user-read-email"

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
    return {"message": "Hello World"}


@router.get("/login")
async def login():
    spotify_credentials = SpotifyAppCredentials()
    redirect_url = "https://f8fff8a5d3e0.ngrok.app/api/v0/spotify/callback"

    return RedirectResponse(
        f"https://accounts.spotify.com/authorize?"
        f"response_type=code&client_id={spotify_credentials.client_id}&"
        f"scope={spotify_credentials.scope}&redirect_uri={redirect_url}&"
        f"state={spotify_credentials.state}"
    )


@router.get("/callback")
async def callback(code: str, state: str):
    spotify_credentials = SpotifyAppCredentials()
    redirect_url = "https://f8fff8a5d3e0.ngrok.app/api/v0/spotify/callback"
    if state != spotify_credentials.state:
        return Response("State Mismatch", status_code=403)

    async with AsyncClient() as client:
        # Build the Basic Auth header value
        auth_string = (
            f"{spotify_credentials.client_id}:{spotify_credentials.client_secret}"
        )
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

        response = await client.post(
            url="https://accounts.spotify.com/api/token",
            headers={
                # "content-type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {auth_base64}",
            },
            data={
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_url,
            },
        )

        try:
            response.raise_for_status()
        except BaseException as e:
            return Response(
                f"Spotify returned this -- {str(e)}", status_code=response.status_code
            )

        user_credentials = SpotifyUserCredentials(**response.json())

        return f"OAuth Flow completed successfuly {user_credentials}"
