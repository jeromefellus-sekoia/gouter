import json
from fastapi import WebSocket


WEBSOCKETS: list[WebSocket] = []


def on_ws_receive(ws: WebSocket, msg):
    print(ws)
    print(msg)


async def notify_all(msg):
    if not isinstance(msg, str):
        msg = json.dumps(msg)
    for ws in WEBSOCKETS:
        await ws.send(msg)
