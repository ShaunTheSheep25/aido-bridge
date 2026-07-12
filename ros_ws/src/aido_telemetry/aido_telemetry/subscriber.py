import rclpy
from rclpy.node import Node

from aido_telemetry.msg import TelemetryMsg


class TelemetrySubscriber(Node):
    def __init__(self) -> None:
        super().__init__("telemetry_subscriber")
        self.subscription = self.create_subscription(
            TelemetryMsg,
            "/aido/telemetry",
            self.listener_callback,
            10,
        )
        self.get_logger().info("Telemetry subscriber started")

    def listener_callback(self, msg: TelemetryMsg) -> None:
        self.get_logger().info(
            f"Received — pos: {msg.position}, battery: {msg.battery}%, "
            f"heading: {msg.heading}°, ts: {msg.timestamp}"
        )


def main() -> None:
    rclpy.init()
    node = TelemetrySubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()