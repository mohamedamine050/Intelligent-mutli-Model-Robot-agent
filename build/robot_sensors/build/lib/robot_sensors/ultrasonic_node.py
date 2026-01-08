#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
import serial
import time


class UltrasonicNode(Node):
    """
    Reads ultrasonic sensor data from Arduino via Serial
    Publishes sensor_msgs/Range on /ultrasonic/front
    
    Expected Arduino format:  "U: <distance_cm>\n"
    Example: "U:25. 4\n"
    """
    
    def __init__(self):
        super().__init__('ultrasonic_node')
        
        # Parameters
        self.declare_parameter('serial_port', '/dev/ttyACM0')
        self.declare_parameter('baudrate', 115200)
        self.declare_parameter('frame_id', 'ultrasonic_link')
        self.declare_parameter('min_range', 0.02)  # 2 cm
        self.declare_parameter('max_range', 4.0)   # 4 meters
        self.declare_parameter('field_of_view', 0.5)  # ~30 degrees in radians
        self.declare_parameter('update_rate', 10.0)  # Hz
        
        # Get parameters
        self.serial_port = self.get_parameter('serial_port').value
        self.baudrate = self.get_parameter('baudrate').value
        self.frame_id = self.get_parameter('frame_id').value
        self. min_range = self.get_parameter('min_range').value
        self.max_range = self.get_parameter('max_range').value
        self.field_of_view = self.get_parameter('field_of_view').value
        update_rate = self.get_parameter('update_rate').value
        
        # Serial connection
        self.serial_conn = None
        self.connect_serial()
        
        # Publisher
        self.range_pub = self.create_publisher(Range, '/ultrasonic/front', 10)
        
        # Timer
        self.create_timer(1.0 / update_rate, self.read_and_publish)
        
        self.get_logger().info(f'Ultrasonic node started on {self.serial_port}')
    
    def connect_serial(self):
        """Establish serial connection with Arduino"""
        try:
            self.serial_conn = serial.Serial(
                self.serial_port,
                self.baudrate,
                timeout=0.5
            )
            time.sleep(2)  # Wait for Arduino reset
            self.get_logger().info('Serial connection established')
        except serial.SerialException as e:
            self.get_logger().error(f'Failed to connect to Arduino: {e}')
            self.serial_conn = None
    
    def read_and_publish(self):
        """Read ultrasonic data from Arduino and publish Range message"""
        
        if self.serial_conn is None or not self.serial_conn.is_open:
            self.get_logger().warn('Serial not connected, attempting reconnect... ', throttle_duration_sec=5.0)
            self.connect_serial()
            return
        
        try:
            # Read line from Arduino
            if self.serial_conn. in_waiting > 0:
                line = self.serial_conn.readline().decode('utf-8').strip()
                
                # Expected format: "U: 25.4"
                if line.startswith('U:'):
                    distance_cm = float(line[2:])
                    distance_m = distance_cm / 100.0
                    
                    # Publish Range message
                    self.publish_range(distance_m)
        
        except (serial.SerialException, ValueError, UnicodeDecodeError) as e:
            self.get_logger().warn(f'Error reading ultrasonic:  {e}', throttle_duration_sec=5.0)
            self.serial_conn = None
    
    def publish_range(self, distance):
        """Publish Range message"""
        msg = Range()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = self. frame_id
        msg.radiation_type = Range.ULTRASOUND
        msg.field_of_view = self.field_of_view
        msg.min_range = self.min_range
        msg.max_range = self. max_range
        msg.range = distance
        
        self. range_pub.publish(msg)
    
    def destroy_node(self):
        """Clean shutdown"""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = UltrasonicNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node. destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()