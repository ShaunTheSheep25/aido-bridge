import threading

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from aido_telemetry.msg import TelemetryMsg

from .state import telemetry_state


class TelemetryBridgeNode(Node):
    def __init__(self) -> None:
        super().__init__("aido_bridge_node")
        # Matches the publisher's default profile: RELIABLE, KEEP_LAST, depth 10
        qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )
        self.create_subscription(TelemetryMsg, "/aido/telemetry", self._on_msg, qos)
        self.get_logger().info("aido-bridge subscribed to /aido/telemetry")

    def _on_msg(self, msg: TelemetryMsg) -> None:
        telemetry_state.update(
            position=msg.position,
            battery=msg.battery,
            heading=msg.heading,
            timestamp=msg.timestamp,
        )


_ros_thread: threading.Thread | None = None
_node: TelemetryBridgeNode | None = None


def start_ros_node() -> TelemetryBridgeNode:
    global _ros_thread, _node
    rclpy.init()
    _node = TelemetryBridgeNode()
    _ros_thread = threading.Thread(target=rclpy.spin, args=(_node,), daemon=True)
    _ros_thread.start()
    return _node


def shutdown_ros_node() -> None:
    global _node
    if _node is not None:
        _node.destroy_node()
    rclpy.shutdown()