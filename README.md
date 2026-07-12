# Aido (Bridge)

This is a FastAPI process that bridges ROS 2 telemetry onto the web: it subscribes to the `/aido/telemetry` topic of `aido_telemetry` via `rclpy` and re-publishes the same data over a plain REST endpoint and a WebSocket, so that a browser with zero ROS install can see live rover telemetry. Built as the Week 6 REST-ROS bridge deliverable, anchored conceptually to InGen Dynamics' Aido Rover.

## How to run it

1. Clone the bridge repo

```bash
git clone https://github.com/ShaunTheSheep25/aido-bridge.git
cd aido-bridge
```

2. Build the docker images of the bridge + publisher using docker-compose and start them up.

```bash
docker-compose up --build publisher bridge
```

3. For manual testing, verify that live telemetry JSONs are being sent periodically over the bridge API:

```bash
curl localhost:8000/telemetry/latest
```

For the WebSocket, open `http://localhost:8000/docs` in a browser, open dev tools > Console, and run:

```js
const ws = new WebSocket("ws://localhost:8000/ws/telemetry");
ws.onmessage = (e) => console.log(JSON.parse(e.data));
```

## How to test it (w/ pytest)

Do note that you must build + start the publisher and bridge before you can test it with pytest.

```bash
docker-compose run --rm bridge bash -c "source /opt/ros/humble/setup.bash && source /ros_ws/install/setup.bash && python3 -m pytest tests/ -v"
```

## Known limitations + What I'd do next

- The WebSocket is poll-based (checks state every 100ms) rather than a true push from the ROS callback into asyncio (this was simpler
to implement, but this was done at the cost of up to ~100ms of extra latency versus a `call_soon_threadsafe`/`asyncio.Queue` approach, so I'll probably look into that)
- `ros_ws/src/aido_telemetry` is a manually copied duplicate of the real `aido_telemetry` repo, not a git submodule — it will silently go stale if the source repo changes and this copy isn't re-synced. To remedy this, I'd replace the manual `aido_telemetry` copy with a git submodule, so the bridge always builds against a pinned, explicit version of the upstream package.
- No CI pipeline has been implemented as of yet, so I'd add a GitHub Actions workflow that builds the image and runs the pytest suite
on every push.
- Requires a FastRTPS UDP-only transport override (`config/fastrtps-udp-only.xml`) to work reliably in Docker; omitting it can cause topic discovery to succeed while actual message delivery silently hangs.
- If the ROS publisher dies mid-session, the bridge correctly keeps serving the last known value rather than crashing, but there's no explicit "stale" flag - a client can't currently tell fresh data from data that stopped updating an hour ago. So, I'd add a `stale: bool` / `age_seconds` field to the REST and WS payloads, computed from `received_at`, so clients can distinguish live data from a dead feed.
