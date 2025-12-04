import base64
from pathlib import Path
from fastapi import Response
from fastapi.responses import HTMLResponse, RedirectResponse
from httpx import AsyncClient
from values.spotify_values import SpotifyAppCredentials, SpotifyUserCredentials


def login():
    spotify_credentials = SpotifyAppCredentials()

    return RedirectResponse(
        f"https://accounts.spotify.com/authorize?"
        f"response_type=code&client_id={spotify_credentials.client_id}&"
        f"scope={spotify_credentials.scope}&redirect_uri={spotify_credentials.redirect_url}&"
        f"state={spotify_credentials.state}"
    )


async def callback(code: str, state: str):
    spotify_credentials = SpotifyAppCredentials()

    if state != spotify_credentials.state:
        error_template_path = Path("static/error.html")
        error_html = error_template_path.read_text()

        error_html = error_html.replace("{status_code}", str(403))
        error_html = error_html.replace("{error_message}", "State Mismatch")

        return HTMLResponse(content=error_html, status_code=403)

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
