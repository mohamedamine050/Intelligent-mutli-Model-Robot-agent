#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs. msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
import message_filters


class StereoDepthNode(Node):
    """
    Takes left and right images from ESP32-CAM
    Computes disparity map using stereo matching
    Publishes depth image
    
    NOTE: Cameras MUST be calibrated for accurate results!
    Use camera_calibration package first. 
    """
    
    def __init__(self):
        super().__init__('stereo_depth_node')
        
        # Parameters
        self.declare_parameter('baseline', 0.075)  # Distance between cameras (meters) - MEASURE THIS!
        self.declare_parameter('focal_length', 500.0)  # Pixels - from calibration
        self.declare_parameter('min_disparity', 0)
        self.declare_parameter('num_disparities', 16 * 5)  # Must be divisible by 16
        self. declare_parameter('block_size', 15)  # Odd number
        
        # Get parameters
        self. baseline = self.get_parameter('baseline').value
        self.focal_length = self.get_parameter('focal_length').value
        self.min_disparity = self.get_parameter('min_disparity').value
        self.num_disparities = self.get_parameter('num_disparities').value
        self.block_size = self.get_parameter('block_size').value
        
        # CV Bridge
        self.bridge = CvBridge()
        
        # Stereo matcher (SGBM is better than BM)
        self.stereo = cv2.StereoSGBM_create(
            minDisparity=self.min_disparity,
            numDisparities=self.num_disparities,
            blockSize=self.block_size,
            P1=8 * 3 * self.block_size**2,
            P2=32 * 3 * self. block_size**2,
            disp12MaxDiff=1,
            uniquenessRatio=10,
            speckleWindowSize=100,
            speckleRange=32,
            mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
        )
        
        # Subscribers (synchronized)
        self.left_sub = message_filters. Subscriber(self, Image, '/camera/left/image_raw')
        self.right_sub = message_filters. Subscriber(self, Image, '/camera/right/image_raw')
        
        # Time synchronizer
        self.ts = message_filters.ApproximateTimeSynchronizer(
            [self.left_sub, self. right_sub],
            queue_size=10,
            slop=0.1  # 100ms tolerance
        )
        self.ts.registerCallback(self. stereo_callback)
        
        # Publishers
        self.depth_pub = self.create_publisher(Image, '/stereo/depth', 10)
        self.disparity_pub = self.create_publisher(Image, '/stereo/disparity', 10)
        
        self.get_logger().info('Stereo depth node started')
    
    def stereo_callback(self, left_msg, right_msg):
        """Process stereo pair and compute depth"""
        
        try:
            # Convert to OpenCV
            left_img = self.bridge.imgmsg_to_cv2(left_msg, desired_encoding='bgr8')
            right_img = self.bridge.imgmsg_to_cv2(right_msg, desired_encoding='bgr8')
            
            # Convert to grayscale
            left_gray = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY)
            right_gray = cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY)
            
            # Compute disparity
            disparity = self.stereo.compute(left_gray, right_gray).astype(np.float32) / 16.0
            
            # Convert disparity to depth
            # depth = (baseline * focal_length) / disparity
            # Avoid division by zero
            depth = np.where(
                disparity > 0,
                (self. baseline * self.focal_length) / disparity,
                0.0
            )
            
            # Clip to reasonable range (0.3m to 10m)
            depth = np. clip(depth, 0.3, 10.0)
            
            # Publish depth image (as 32FC1)
            depth_msg = self.bridge.cv2_to_imgmsg(depth, encoding='32FC1')
            depth_msg.header = left_msg.header
            depth_msg.header.frame_id = 'camera_depth_frame'
            self.depth_pub.publish(depth_msg)
            
            # Publish disparity for visualization
            disparity_normalized = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            disparity_msg = self.bridge.cv2_to_imgmsg(disparity_normalized, encoding='mono8')
            disparity_msg.header = left_msg.header
            self.disparity_pub.publish(disparity_msg)
        
        except Exception as e: 
            self.get_logger().error(f'Stereo processing error: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = StereoDepthNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__': 
    main()