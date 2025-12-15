from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from gateways import spotify_gateway
from gateways.app_values import AlbumsPriceRequest
from gateways import discogs_gateway

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
    return await discogs_gateway.get_price_of_albums(albums_price_request)


@router.get("/all_albums_price")
async def get_all_ambums_price(request: Request):
    return await discogs_gateway.get_all_ambums_price(request=request)


@router.websocket("/ws/calculate_all_albums")
async def websocket_calculate_all_albums(websocket: WebSocket):
    await websocket.accept()

    try:
        # Get access token from cookies
        access_token = websocket.cookies.get("spotify_access_token")

        if not access_token:
            await websocket.send_json({"error": "No access token provided"})
            await websocket.close()
            return

        # Stream albums one by one without loading all into memory
        async for (
            album_item,
            current_index,
            total_count,
        ) in spotify_gateway.stream_albums_with_token(access_token):
            try:
                # Send total count on first album
                if current_index == 1:
                    await websocket.send_json(
                        {"type": "total", "total_albums": total_count}
                    )

                album = album_item.album
                artist = album.artists[0].name if album.artists else "Unknown Artist"
                album_name = album.name

                # Get price for this album
                album_price, was_price_found = await discogs_gateway.get_price_of_album(
                    artist, album_name
                )

                # Send album data with price
                await websocket.send_json(
                    {
                        "type": "album",
                        "index": current_index,
                        "total": total_count,
                        "album": {
                            "name": album_name,
                            "artist": artist,
                            "price": float(album_price),
                            "valid": was_price_found,
                            "image": album.images[0].url if album.images else None,
                            "release_date": album.release_date,
                        },
                    }
                )

            except Exception as e:
                await websocket.send_json(
                    {"type": "error", "message": f"Error processing album: {str(e)}"}
                )

        # Send completion message
        await websocket.send_json({"type": "complete"})

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        try:
            await websocket.send_json({"error": str(e)})
        except BaseException:
            pass
    finally:
        try:
            await websocket.close()
        except BaseException:
            pass
