import base64
from fastapi import Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from httpx import AsyncClient
from dotenv import load_dotenv
from values.spotify_values import (
    SpotifyAppCredentials,
    SpotifyUser,
    SpotifyUserCredentials,
)
from typing import Optional

load_dotenv()

templates = Jinja2Templates(directory="static")


async def root(request: Request):
    access_token = request.cookies.get("spotify_access_token")

    if access_token:
        spotify_user = await validate_access_token(access_token)

        if spotify_user:
            return templates.TemplateResponse(
                "home.html",
                {
                    "request": request,
                    "display_name": spotify_user.display_name,
                    "username": spotify_user.id,
                },
            )

    return FileResponse("static/index.html")


def login():
    spotify_credentials = SpotifyAppCredentials()

    return RedirectResponse(
        f"https://accounts.spotify.com/authorize?"
        f"response_type=code&client_id={spotify_credentials.client_id}&"
        f"scope={spotify_credentials.scope}&redirect_uri={spotify_credentials.redirect_url}&"
        f"state={spotify_credentials.state}"
    )


async def callback(request: Request, code: str, state: str):
    spotify_credentials = SpotifyAppCredentials()

    if state != spotify_credentials.state:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "status_code": 403,
                "error_message": "State Mismatch",
            },
            status_code=403,
        )

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
            return templates.TemplateResponse(
                "error.html",
                {
                    "request": request,
                    "status_code": response.status_code,
                    "error_message": str(e),
                },
                status_code=response.status_code,
            )

        user_credentials = SpotifyUserCredentials(**response.json())

        html_response = templates.TemplateResponse(
            "spotify_oauth_success.html",
            {"request": request},
            status_code=200,
        )

        html_response.set_cookie(
            key="spotify_access_token",
            value=user_credentials.access_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )

        html_response.set_cookie(
            key="spotify_refresh_token",
            value=user_credentials.refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )

        html_response.set_cookie(
            key="spotify_expires_in", value=str(user_credentials.expires_in)
        )

        return html_response


async def validate_access_token(access_token: str) -> Optional[SpotifyUser]:
    """
    Validates the Spotify access token by making a request to the /me endpoint.
    Returns user data if valid, None if invalid.
    """
    async with AsyncClient() as client:
        try:
            response = await client.get(
                url="https://api.spotify.com/v1/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                },
            )

            response.raise_for_status()
            return SpotifyUser(**response.json())
        except Exception:
            return None
