#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial
import time


class WheelDriver(Node):
    """
    Subscribes to /cmd_vel_safe (Twist)
    Converts to left/right wheel speeds
    Sends to Arduino via Serial
    """
    
    def __init__(self):
        super().__init__('wheel_driver')
        
        # Declare parameters
        self.declare_parameter('serial_port', '/dev/ttyACM0')
        self.declare_parameter('baudrate', 115200)
        self.declare_parameter('wheel_separation', 0.16)  # meters (from URDF)
        self.declare_parameter('wheel_radius', 0.033)     # meters (from URDF)
        self.declare_parameter('max_linear_speed', 0.5)   # m/s
        self.declare_parameter('max_angular_speed', 2.0)  # rad/s
        self.declare_parameter('pwm_max', 255)
        self.declare_parameter('pwm_min', 80)  # Minimum PWM to move
        
        # Get parameters
        self.serial_port = self.get_parameter('serial_port').value
        self.baudrate = self.get_parameter('baudrate').value
        self.wheel_separation = self.get_parameter('wheel_separation').value
        self. wheel_radius = self.get_parameter('wheel_radius').value
        self.max_linear = self.get_parameter('max_linear_speed').value
        self.max_angular = self.get_parameter('max_angular_speed').value
        self.pwm_max = self.get_parameter('pwm_max').value
        self.pwm_min = self.get_parameter('pwm_min').value
        
        # Initialize serial connection
        self.serial_conn = None
        self.connect_serial()
        
        # Subscribe to velocity commands
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel_safe',
            self.cmd_vel_callback,
            10
        )
        
        self.get_logger().info(f'Wheel driver started on {self.serial_port}')
    
    def connect_serial(self):
        """Establish serial connection with Arduino"""
        try:
            self.serial_conn = serial. Serial(
                self.serial_port,
                self.baudrate,
                timeout=1
            )
            time.sleep(2)  # Wait for Arduino to reset
            self.get_logger().info('Serial connection established')
        except serial.SerialException as e:
            self.get_logger().error(f'Failed to connect to Arduino: {e}')
            self.serial_conn = None
    
    def cmd_vel_callback(self, msg):
        """Convert Twist to wheel speeds and send to Arduino"""
        
        # Extract linear and angular velocities
        v = msg.linear.x   # m/s
        w = msg.angular.z  # rad/s
        
        # Clamp to max speeds
        v = max(-self. max_linear, min(self. max_linear, v))
        w = max(-self.max_angular, min(self.max_angular, w))
        
        # Differential drive kinematics
        # v_left = v - (w * wheel_separation / 2)
        # v_right = v + (w * wheel_separation / 2)
        v_left = v - (w * self.wheel_separation / 2.0)
        v_right = v + (w * self.wheel_separation / 2.0)
        
        # Convert m/s to PWM (-255 to +255)
        # Max speed (m/s) corresponds to PWM_MAX
        pwm_left = self.velocity_to_pwm(v_left)
        pwm_right = self.velocity_to_pwm(v_right)
        
        # Send to Arduino
        self.send_to_arduino(pwm_left, pwm_right)
        
        # Log (optional, comment out in production)
        # self.get_logger().debug(f'v={v:.2f}, w={w:.2f} -> L={pwm_left}, R={pwm_right}')
    
    def velocity_to_pwm(self, velocity):
        """Convert linear velocity (m/s) to PWM value"""
        # Map velocity to PWM range
        # velocity range: [-max_linear, +max_linear]
        # PWM range: [-pwm_max, +pwm_max]
        
        if abs(velocity) < 0.01:  # Dead zone
            return 0
        
        # Linear mapping
        pwm = int((velocity / self.max_linear) * self.pwm_max)
        
        # Apply minimum PWM (to overcome friction)
        if pwm > 0 and pwm < self.pwm_min:
            pwm = self.pwm_min
        elif pwm < 0 and pwm > -self.pwm_min:
            pwm = -self.pwm_min
        
        # Clamp
        pwm = max(-self. pwm_max, min(self.pwm_max, pwm))
        
        return pwm
    
    def send_to_arduino(self, left_pwm, right_pwm):
        """Send PWM commands to Arduino via Serial"""
        if self.serial_conn is None or not self.serial_conn.is_open:
            self.get_logger().warn('Serial not connected, attempting reconnect...')
            self.connect_serial()
            return
        
        try:
            # Format: "L: <left_pwm>;R:<right_pwm>\n"
            command = f"L:{left_pwm};R:{right_pwm}\n"
            self.serial_conn. write(command.encode('utf-8'))
        except serial.SerialException as e:
            self.get_logger().error(f'Serial write error: {e}')
            self.serial_conn = None
    
    def destroy_node(self):
        """Clean shutdown:  stop motors"""
        self.get_logger().info('Shutting down, stopping motors...')
        self.send_to_arduino(0, 0)
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = WheelDriver()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt: 
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__': 
    main()