import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool


class PatrolSpeedService(Node):
    def __init__(self) -> None:
        super().__init__("patrol_speed_service")
        self.srv = self.create_service(
            SetBool,
            "/set_patrol_speed",
            self.handle_set_speed,
        )
        self.get_logger().info("Patrol speed service ready")

    def handle_set_speed(
        self, request: SetBool.Request, response: SetBool.Response
    ) -> SetBool.Response:
        self.get_logger().info(f"Speed request received: {request.data}")
        response.success = True
        response.message = "Speed updated successfully"
        return response


def main() -> None:
    rclpy.init()
    node = PatrolSpeedService()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()