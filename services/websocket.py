import pusher
from pydantic_settings import BaseSettings


class SoketiSettings(BaseSettings):
    host: str = "localhost"
    port: int = 6001
    app_id: str = "app_id"
    key: str = "app_key"
    secret: str = "app_secret"
    use_tls: bool = True
    cluster: str = ""

    class Config:
        env_prefix = "SOKETI_DEFAULT_APP_"


soketi_settings = SoketiSettings()


def get_pusher_client() -> pusher.Pusher:
    """
    Get a Pusher client instance configured for Soketi.

    Returns:
        pusher.Pusher: Configured Pusher client instance.
    """
    return pusher.Pusher(
        app_id=soketi_settings.app_id,
        key=soketi_settings.key,
        secret=soketi_settings.secret,
        host=soketi_settings.host,
        port=soketi_settings.port,
        ssl=soketi_settings.use_tls,
        cluster=soketi_settings.cluster,
    )
    
client = get_pusher_client()

async def trigger_event(
    channel: str,
    event: str,
    data: dict,
    socket_id: str | None = None
) -> dict:
    """
    Trigger an event on a specific channel via Soketi.

    Args:
        channel: The channel name to trigger the event on.
        event: The event name to trigger.
        data: The data payload to send with the event.
        socket_id: Optional socket ID to exclude from receiving the event.

    Returns:
        dict: Response from the Pusher API.
    """
    
    return client.trigger(channel, event, data, socket_id)


async def trigger_batch(events: list[dict]) -> dict:
    """
    Trigger multiple events in a single API call.

    Args:
        events: List of event dictionaries, each containing 'channel', 'name', and 'data' keys.
               Example: [
                   {'channel': 'my-channel', 'name': 'my-event', 'data': {'message': 'hello'}},
                   {'channel': 'other-channel', 'name': 'other-event', 'data': {'foo': 'bar'}}
               ]

    Returns:
        dict: Response from the Pusher API.
    """
    return client.trigger_batch(events)


def authenticate_channel(
    channel: str,
    socket_id: str,
    custom_data: dict | None = None
) -> str:
    """
    Generate authentication signature for private/presence channels.

    Args:
        channel: The channel name to authenticate.
        socket_id: The socket ID requesting authentication.
        custom_data: Optional custom data for presence channels.

    Returns:
        str: Authentication signature.
    """
    
    if custom_data:
        return client.authenticate(channel, socket_id, custom_data)
    return client.authenticate(channel, socket_id)
