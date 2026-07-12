cmake_minimum_required(VERSION 3.8)
project(aido_telemetry)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/TelemetryMsg.msg"
  "srv/SetPatrolSpeed.srv"
)

ament_package()