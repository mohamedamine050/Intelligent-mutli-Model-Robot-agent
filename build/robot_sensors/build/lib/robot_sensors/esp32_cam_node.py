#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge
import cv2
import numpy as np
import requests
from io import BytesIO


class ESP32CamNode(Node):
    """
    Reads MJPEG stream from ESP32-CAM via HTTP
    Publishes sensor_msgs/Image
    
    ESP32-CAM must be configured to stream on: 
    http://<IP>: 81/stream (default MJPEG endpoint)
    """
    
    def __init__(self):
        super().__init__('esp32_cam_node')
        
        # Parameters
        self.declare_parameter('camera_name', 'camera')  # 'left' or 'right'
        self.declare_parameter('camera_ip', '192.168.1.100')
        self.declare_parameter('stream_port', 81)
        self.declare_parameter('frame_id', 'camera_link')
        self.declare_parameter('publish_rate', 30.0)  # Hz
        self.declare_parameter('image_width', 640)
        self.declare_parameter('image_height', 480)
        
        # Get parameters
        self.camera_name = self.get_parameter('camera_name').value
        self.camera_ip = self.get_parameter('camera_ip').value
        self.stream_port = self.get_parameter('stream_port').value
        self.frame_id = self.get_parameter('frame_id').value
        self. publish_rate = self.get_parameter('publish_rate').value
        self.image_width = self.get_parameter('image_width').value
        self.image_height = self.get_parameter('image_height').value
        
        # CV Bridge
        self.bridge = CvBridge()
        
        # Publishers
        self.image_pub = self.create_publisher(
            Image, 
            f'/camera/{self. camera_name}/image_raw', 
            10
        )
        self.camera_info_pub = self.create_publisher(
            CameraInfo,
            f'/camera/{self.camera_name}/camera_info',
            10
        )
        
        # Stream URL
        self.stream_url = f'http://{self.camera_ip}:{self.stream_port}/stream'
        
        # Start streaming
        self.stream = None
        self.connect_stream()
        
        # Timer to read frames
        self.create_timer(1.0 / self.publish_rate, self.read_and_publish)
        
        self.get_logger().info(f'ESP32-CAM {self.camera_name} node started:  {self.stream_url}')
    
    def connect_stream(self):
        """Connect to ESP32-CAM MJPEG stream"""
        try:
            self.stream = requests.get(self.stream_url, stream=True, timeout=5)
            self.bytes_data = b''
            self.get_logger().info('Stream connected')
        except Exception as e:
            self.get_logger().error(f'Failed to connect to stream: {e}')
            self.stream = None
    
    def read_and_publish(self):
        """Read frame from MJPEG stream and publish"""
        
        if self.stream is None:
            self.get_logger().warn('Stream not connected, retrying... ', throttle_duration_sec=5.0)
            self.connect_stream()
            return
        
        try:
            # Read chunk from stream
            for chunk in self.stream.iter_content(chunk_size=1024):
                self.bytes_data += chunk
                
                # Find JPEG boundaries
                a = self.bytes_data.find(b'\xff\xd8')  # JPEG start
                b = self. bytes_data.find(b'\xff\xd9')  # JPEG end
                
                if a != -1 and b != -1:
                    jpg = self.bytes_data[a:b+2]
                    self.bytes_data = self.bytes_data[b+2:]
                    
                    # Decode JPEG
                    img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    
                    if img is not None:
                        # Resize if needed
                        img = cv2.resize(img, (self.image_width, self.image_height))
                        
                        # Publish image
                        self.publish_image(img)
                        
                        # Only process one frame per timer call
                        break
        
        except Exception as e: 
            self.get_logger().error(f'Error reading stream: {e}')
            self.stream = None
    
    def publish_image(self, cv_image):
        """Publish ROS Image message"""
        try:
            # Convert to ROS Image
            msg = self.bridge.cv2_to_imgmsg(cv_image, encoding='bgr8')
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = self.frame_id
            
            self.image_pub.publish(msg)
            
            # Publish camera info (simple, you should calibrate!)
            self.publish_camera_info()
        
        except Exception as e: 
            self.get_logger().error(f'Error publishing image: {e}')
    
    def publish_camera_info(self):
        """Publish basic camera info (should be replaced with calibration)"""
        info = CameraInfo()
        info.header.stamp = self.get_clock().now().to_msg()
        info.header.frame_id = self.frame_id
        info. width = self.image_width
        info.height = self.image_height
        
        # Placeholder intrinsics (MUST BE CALIBRATED!)
        info.k = [500.0, 0.0, 320.0,
                  0.0, 500.0, 240.0,
                  0.0, 0.0, 1.0]
        
        info. d = [0.0, 0.0, 0.0, 0.0, 0.0]  # No distortion (should calibrate!)
        
        info.r = [1.0, 0.0, 0.0,
                  0.0, 1.0, 0.0,
                  0.0, 0.0, 1.0]
        
        info.p = [500.0, 0.0, 320.0, 0.0,
                  0.0, 500.0, 240.0, 0.0,
                  0.0, 0.0, 1.0, 0.0]
        
        self.camera_info_pub.publish(info)
    
    def destroy_node(self):
        if self.stream:
            self. stream.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = ESP32CamNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt: 
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__': 
    main()