FROM osrf/ros:humble-desktop

WORKDIR /ros_ws
COPY ros_ws/src /ros_ws/src

RUN /bin/bash -c "source /opt/ros/humble/setup.bash && \
    colcon build --packages-select aido_telemetry"

RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install --upgrade pip setuptools wheel

WORKDIR /app
COPY config/fastrtps-udp-only.xml /config/fastrtps-udp-only.xml
COPY pyproject.toml ./
COPY src ./src
COPY tests ./tests
RUN pip3 install -e ".[dev]"

COPY docker-entrypoint.sh ./
RUN chmod +x docker-entrypoint.sh
CMD ["./docker-entrypoint.sh"]