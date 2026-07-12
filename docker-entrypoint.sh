#!/bin/bash
source /opt/ros/humble/setup.bash
source /ros_ws/install/setup.bash
exec uvicorn aido_bridge.main:app --host 0.0.0.0 --port 8000