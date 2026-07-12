import json
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from aido_telemetry.msg import TelemetryMsg


class TelemetryPublisher(Node):
    def __init__(self) -> None:
        super().__init__("telemetry_publisher")
        self.publisher_ = self.create_publisher(TelemetryMsg, "/aido/telemetry", 10)
        self.json_publisher_ = self.create_publisher(
            String, "/aido/telemetry/json", 10
        )
        self.timer = self.create_timer(0.1, self.publish_telemetry)
        self.heading = 0.0
        self.get_logger().info("Telemetry publisher started at 10 Hz")

    def publish_telemetry(self) -> None:
        msg = TelemetryMsg()
        msg.position = 13.0827
        msg.battery = 85.0
        msg.heading = self.heading
        msg.timestamp = int(time.time())
        self.publisher_.publish(msg)

        json_msg = String()
        json_msg.data = json.dumps({
            "position": msg.position,
            "battery": msg.battery,
            "heading": msg.heading,
            "timestamp": msg.timestamp,
        })
        self.json_publisher_.publish(json_msg)

        self.heading = (self.heading + 1.0) % 360.0
        self.get_logger().info(
            f"Published — heading: {msg.heading}° battery: {msg.battery}%"
        )


def main() -> None:
    rclpy.init()
    node = TelemetryPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()