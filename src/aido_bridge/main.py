import asyncio
import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from .ros_node import start_ros_node, shutdown_ros_node
from .state import telemetry_state


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_ros_node()
    yield
    shutdown_ros_node()


app = FastAPI(title="aido-bridge", lifespan=lifespan)


@app.get("/telemetry/latest")
async def get_latest():
    data = telemetry_state.get()
    if data is None:
        return {"detail": "no telemetry received yet"}
    return data


@app.websocket("/ws/telemetry")
async def ws_telemetry(websocket: WebSocket):
    await websocket.accept()
    last_sent = None
    try:
        while True:
            data = telemetry_state.get()
            if data and data != last_sent:
                await websocket.send_text(json.dumps(data))
                last_sent = data
            await asyncio.sleep(0.1)  # matches the publisher's 10 Hz rate
    except WebSocketDisconnect:
        pass