import asyncio
import json
from fastapi import WebSocket


WEBSOCKETS: list[WebSocket] = []
USERS: set[str] = set()


def on_ws_receive(ws: WebSocket, msg):
    ...


async def notify_all(msg):
    for ws in WEBSOCKETS:
        await ws.send_json(msg)
