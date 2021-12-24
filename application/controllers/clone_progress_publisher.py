# Refs:
# https://fastapi.tiangolo.com/advanced/websockets/
# https://github.com/encode/broadcaster
# https://dev.to/sangarshanan/realtime-channels-with-fastapi-broadcaster-47jh

from broadcaster import Broadcast
from fastapi import APIRouter, WebSocket
from pydantic import BaseModel
from websockets.exceptions import ConnectionClosedOK

broadcast = Broadcast("memory://")

router = APIRouter(on_startup=[broadcast.connect], on_shutdown=[broadcast.disconnect])


class ProgressMessage(BaseModel):
    channel: str
    data: str


@router.post("/progress/")
async def publish_clone_progress(progress: ProgressMessage):
    await broadcast.publish(channel=progress.channel, message=progress.data)


@router.websocket("/progress/{channel}")
async def brocast_clone_progress(websocket: WebSocket, channel: str):
    await websocket.accept()
    try:
        async with broadcast.subscribe(channel=channel) as subscriber:
            async for event in subscriber:
                await websocket.send_text(event.message)
    except ConnectionClosedOK:
        pass
