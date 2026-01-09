import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from r2d2_audio.engines.gemini_client import GeminiClient

class LLMNode(Node):
    def __init__(self):
        super().__init__('llm_node')
        self.llm = GeminiClient()
        
        self.sub = self.create_subscription(
            String,
            '/audio/asr_text',
            self.callback,
            10
        )
        
        self.pub = self.create_publisher(
            String,
            '/llm/response',
            10
        )
        
        self.get_logger().info("🤖 Gemini LLM Node started")
    
    def callback(self, msg):
        reply = self.llm.generate(msg.data)  # Changed from ask() to generate()
        out = String()
        out.data = reply
        self.pub.publish(out)

def main():
    rclpy.init()
    node = LLMNode()
    rclpy.spin(node)
    rclpy.shutdown()
