import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from r2d2_audio.engines.tts_engine import TTSEngine

class TTSNode(Node):
    def __init__(self):
        super().__init__('tts_node')
        self.tts = TTSEngine()

        self.sub = self.create_subscription(
            String,
            '/llm/response',
            self.callback,
            10
        )

        self.get_logger().info("🔊 TTS Node started")

    def callback(self, msg):
        self.tts.speak(msg.data)

def main():
    rclpy.init()
    node = TTSNode()
    rclpy.spin(node)
    rclpy.shutdown()
