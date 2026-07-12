import threading
from datetime import datetime, timezone
from typing import Optional


class TelemetryState:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._latest: Optional[dict] = None

    def update(self, position: float, battery: float, heading: float, timestamp: int) -> None:
        with self._lock:
            self._latest = {
                "position": position,
                "battery": battery,
                "heading": heading,
                "timestamp": timestamp,
                "received_at": datetime.now(timezone.utc).isoformat(),
            }

    def get(self) -> Optional[dict]:
        with self._lock:
            return dict(self._latest) if self._latest else None


telemetry_state = TelemetryState()