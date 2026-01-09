import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from r2d2_audio.engines.stt_engine import STTEngine

class STTNode(Node):
    def __init__(self):
        super().__init__('stt_node')
        self.engine = STTEngine()

        self.publisher = self.create_publisher(String, '/audio/asr_text', 10)
        self.timer = self.create_timer(5.0, self.listen)

        self.get_logger().info("🎤 STT Node started")

    def listen(self):
        text = self.engine.transcribe()
        if text:
            msg = String()
            msg.data = text
            self.publisher.publish(msg)
            self.get_logger().info(f"Recognized: {text}")

def main():
    rclpy.init()
    node = STTNode()
    rclpy.spin(node)
    rclpy.shutdown()
