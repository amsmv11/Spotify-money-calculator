from pydantic import BaseModel
from pydantic_settings import BaseSettings


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
