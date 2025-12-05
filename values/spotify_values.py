from typing import Optional
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class SpotifyAppCredentials(BaseSettings):
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    state: Optional[str] = None
    scope: Optional[str] = None
    redirect_url: Optional[str] = None

    class Config:
        env_prefix = "SPOTIFY_"


class SpotifyUserCredentials(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str


class SpotifyUser(BaseModel):
    display_name: str = "User"
    id: str = "user id"
