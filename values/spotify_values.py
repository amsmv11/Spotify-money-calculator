from typing import List, Optional
from pydantic import BaseModel, ConfigDict
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


class ExternalURL(BaseModel):
    spotify: Optional[str] = None

    model_config = ConfigDict(extra="ignore")


class Image(BaseModel):
    url: str
    height: Optional[int] = None
    width: Optional[int] = None

    model_config = ConfigDict(extra="ignore")


class Restriction(BaseModel):
    reason: Optional[str] = None

    model_config = ConfigDict(extra="ignore")


class ExternalID(BaseModel):
    isrc: Optional[str] = None
    ean: Optional[str] = None
    upc: Optional[str] = None

    model_config = ConfigDict(extra="ignore")


class SimpleArtist(BaseModel):
    external_urls: Optional[ExternalURL] = None
    href: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    uri: Optional[str] = None

    model_config = ConfigDict(extra="ignore")


class LinkedFrom(BaseModel):
    external_urls: Optional[ExternalURL] = None
    href: Optional[str] = None
    id: Optional[str] = None
    type: Optional[str] = None
    uri: Optional[str] = None

    model_config = ConfigDict(extra="ignore")


class TrackItem(BaseModel):
    artists: List[SimpleArtist]
    available_markets: Optional[List[str]] = None
    disc_number: Optional[int] = None
    duration_ms: Optional[int] = None
    explicit: Optional[bool] = None
    external_urls: Optional[ExternalURL] = None
    href: Optional[str] = None
    id: Optional[str] = None
    is_playable: Optional[bool] = None
    linked_from: Optional[LinkedFrom] = None
    restrictions: Optional[Restriction] = None
    name: Optional[str] = None
    preview_url: Optional[str] = None
    track_number: Optional[int] = None
    type: Optional[str] = None
    uri: Optional[str] = None
    is_local: Optional[bool] = None

    model_config = ConfigDict(extra="ignore")


class Tracks(BaseModel):
    href: Optional[str] = None
    limit: Optional[int] = None
    next: Optional[str] = None
    offset: Optional[int] = None
    previous: Optional[str] = None
    total: Optional[int] = None
    items: List[TrackItem]

    model_config = ConfigDict(extra="ignore")


class Copyright(BaseModel):
    text: Optional[str] = None
    type: Optional[str] = None

    model_config = ConfigDict(extra="ignore")


class SpotifyAlbum(BaseModel):
    album_type: Optional[str] = None
    total_tracks: Optional[int] = None
    available_markets: Optional[List[str]] = None
    external_urls: Optional[ExternalURL] = None
    href: Optional[str] = None
    id: Optional[str] = None
    images: Optional[List[Image]] = None
    name: Optional[str] = None
    release_date: Optional[str] = None
    release_date_precision: Optional[str] = None
    restrictions: Optional[Restriction] = None
    type: Optional[str] = None
    uri: Optional[str] = None
    artists: Optional[List[SimpleArtist]] = None
    tracks: Optional[Tracks] = None
    copyrights: Optional[List[Copyright]] = None
    external_ids: Optional[ExternalID] = None
    genres: Optional[List[str]] = None
    label: Optional[str] = None
    popularity: Optional[int] = None

    model_config = ConfigDict(extra="ignore")


class SpotifyAlbumListItem(BaseModel):
    added_at: str
    album: SpotifyAlbum

    model_config = ConfigDict(extra="ignore")


class SpotifyAlbumListResponse(BaseModel):
    href: str
    limit: int
    next: Optional[str] = None
    offset: int
    previous: Optional[str] = None
    items: List[SpotifyAlbumListItem]
    total: int

    model_config = ConfigDict(extra="ignore")
