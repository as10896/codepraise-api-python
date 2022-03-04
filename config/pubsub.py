from app.infrastructure.broadcaster import Broadcast

from .config import Settings, get_settings


def get_pubsub(config: Settings = get_settings()) -> Broadcast:
    if config.environment == "production":
        return Broadcast(config.REDIS_URL)
    else:
        return Broadcast("memory://")
