import json

import pytest
from fastapi.testclient import TestClient

from aido_bridge.main import create_app
from aido_bridge.state import telemetry_state


@pytest.fixture
def client():
    app = create_app(start_ros=False)
    with TestClient(app) as c:
        yield c
    telemetry_state._latest = None 


def test_latest_returns_placeholder_when_empty(client):
    telemetry_state._latest = None
    response = client.get("/telemetry/latest")
    assert response.status_code == 200
    assert response.json() == {"detail": "no telemetry received yet"}


def test_latest_returns_data_once_set(client):
    telemetry_state.update(position=13.08, battery=85.0, heading=42.0, timestamp=1234567890)
    response = client.get("/telemetry/latest")
    assert response.status_code == 200
    body = response.json()
    assert body["position"] == 13.08
    assert body["battery"] == 85.0
    assert body["heading"] == 42.0
    assert body["timestamp"] == 1234567890
    assert "received_at" in body


def test_websocket_streams_current_state_on_connect(client):
    telemetry_state.update(position=1.0, battery=99.0, heading=10.0, timestamp=111)
    with client.websocket_connect("/ws/telemetry") as websocket:
        payload = json.loads(websocket.receive_text())
        assert payload["battery"] == 99.0
        assert payload["heading"] == 10.0


def test_websocket_pushes_new_update_after_connect(client):
    telemetry_state.update(position=1.0, battery=50.0, heading=0.0, timestamp=1)
    with client.websocket_connect("/ws/telemetry") as websocket:
        first = json.loads(websocket.receive_text())
        assert first["battery"] == 50.0

        telemetry_state.update(position=1.0, battery=49.0, heading=1.0, timestamp=2)
        second = json.loads(websocket.receive_text())
        assert second["battery"] == 49.0