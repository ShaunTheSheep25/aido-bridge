import rclpy
from rclpy.node import Node
from aido_telemetry.srv import SetPatrolSpeed


class PatrolSpeedService(Node):
    def __init__(self) -> None:
        super().__init__("patrol_speed_service")
        self.srv = self.create_service(
            SetPatrolSpeed,
            "/set_patrol_speed",
            self.handle_set_speed,
        )
        self.get_logger().info("Patrol speed service ready")

    def handle_set_speed(
        self, request: SetPatrolSpeed.Request, response: SetPatrolSpeed.Response
    ) -> SetPatrolSpeed.Response:
        self.get_logger().info(f"Speed request received: {request.speed}")
        response.ok = True
        return response


def main() -> None:
    rclpy.init()
    node = PatrolSpeedService()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()