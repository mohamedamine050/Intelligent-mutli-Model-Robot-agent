#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped, Quaternion
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster
import serial
import math
import time


class WheelOdometry(Node):
    """
    Publishes odometry based on: 
    - Encoder ticks (if available) from Arduino
    - Or estimated from last cmd_vel (dead reckoning)
    
    Publishes: 
    - /odom (nav_msgs/Odometry)
    - TF odom -> base_footprint
    - /joint_states (optional, for RViz)
    """
    
    def __init__(self):
        super().__init__('wheel_odom')
        
        # Parameters
        self.declare_parameter('serial_port', '/dev/ttyACM0')
        self.declare_parameter('baudrate', 115200)
        self.declare_parameter('wheel_separation', 0.16)
        self.declare_parameter('wheel_radius', 0.033)
        self.declare_parameter('ticks_per_rev', 360)  # If encoders present
        self.declare_parameter('use_encoders', False)  # Set True if encoders available
        self.declare_parameter('odom_frame', 'odom')
        self.declare_parameter('base_frame', 'base_footprint')
        self.declare_parameter('publish_tf', True)
        
        # Get parameters
        self.serial_port = self.get_parameter('serial_port').value
        self. baudrate = self.get_parameter('baudrate').value
        self.wheel_separation = self.get_parameter('wheel_separation').value
        self.wheel_radius = self.get_parameter('wheel_radius').value
        self.ticks_per_rev = self. get_parameter('ticks_per_rev').value
        self. use_encoders = self.get_parameter('use_encoders').value
        self.odom_frame = self.get_parameter('odom_frame').value
        self.base_frame = self. get_parameter('base_frame').value
        self.publish_tf = self.get_parameter('publish_tf').value
        
        # State variables
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.vx = 0.0
        self.vy = 0.0
        self.vth = 0.0
        
        self.last_time = self.get_clock().now()
        
        # Serial connection (for encoders)
        self.serial_conn = None
        if self.use_encoders:
            self.connect_serial()
        
        # Publishers
        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
        self.joint_pub = self.create_publisher(JointState, '/joint_states', 10)
        
        # TF broadcaster
        if self.publish_tf:
            self.tf_broadcaster = TransformBroadcaster(self)
        
        # Timer for odometry updates
        self. create_timer(0.05, self.update_odometry)  # 20 Hz
        
        self.get_logger().info(f'Odometry node started (encoders: {self.use_encoders})')
    
    def connect_serial(self):
        """Connect to Arduino for encoder data"""
        try:
            self.serial_conn = serial.Serial(
                self.serial_port,
                self.baudrate,
                timeout=0.1
            )
            time.sleep(2)
            self.get_logger().info('Serial connected for encoders')
        except serial. SerialException as e:
            self.get_logger().warn(f'Could not connect to Arduino: {e}')
            self.serial_conn = None
    
    def update_odometry(self):
        """Main odometry update loop"""
        current_time = self.get_clock().now()
        dt = (current_time - self. last_time).nanoseconds / 1e9
        
        if dt <= 0:
            return
        
        if self.use_encoders and self.serial_conn:
            # Read encoder data from Arduino
            left_ticks, right_ticks = self.read_encoders()
            
            # Convert ticks to distances
            left_dist = (left_ticks / self.ticks_per_rev) * (2 * math.pi * self. wheel_radius)
            right_dist = (right_ticks / self.ticks_per_rev) * (2 * math.pi * self.wheel_radius)
            
            # Compute velocities
            v_left = left_dist / dt
            v_right = right_dist / dt
            
            # Differential drive forward kinematics
            self.vx = (v_right + v_left) / 2.0
            self.vth = (v_right - v_left) / self.wheel_separation
        else:
            # Dead reckoning:  assume constant velocity from last cmd_vel
            # (You'd need to subscribe to /cmd_vel_safe to get actual commands)
            # For now, we use zero if no encoders
            self.vx = 0.0
            self. vth = 0.0
        
        # Integrate position
        delta_x = self.vx * math.cos(self.theta) * dt
        delta_y = self.vx * math.sin(self.theta) * dt
        delta_theta = self.vth * dt
        
        self.x += delta_x
        self. y += delta_y
        self.theta += delta_theta
        
        # Publish odometry
        self.publish_odometry(current_time)
        
        # Publish TF
        if self. publish_tf:
            self. publish_transform(current_time)
        
        # Publish joint states (for RViz wheel visualization)
        self.publish_joint_states(current_time)
        
        self.last_time = current_time
    
    def read_encoders(self):
        """Read encoder ticks from Arduino (format: E:<left>,<right>)"""
        if not self.serial_conn or not self.serial_conn.is_open:
            return 0, 0
        
        try:
            if self.serial_conn.in_waiting > 0:
                line = self.serial_conn.readline().decode('utf-8').strip()
                if line. startswith('E:'):
                    parts = line[2:].split(',')
                    if len(parts) == 2:
                        return int(parts[0]), int(parts[1])
        except Exception as e:
            self.get_logger().warn(f'Encoder read error: {e}')
        
        return 0, 0
    
    def publish_odometry(self, current_time):
        """Publish odometry message"""
        odom = Odometry()
        odom.header.stamp = current_time. to_msg()
        odom.header.frame_id = self.odom_frame
        odom.child_frame_id = self.base_frame
        
        # Position
        odom. pose.pose.position.x = self.x
        odom. pose.pose.position.y = self.y
        odom. pose.pose.position.z = 0.0
        
        # Orientation (quaternion from theta)
        odom.pose.pose.orientation = self.yaw_to_quaternion(self.theta)
        
        # Velocity
        odom.twist.twist. linear.x = self.vx
        odom.twist.twist.linear.y = 0.0
        odom. twist.twist.angular.z = self.vth
        
        # Covariance (tune these!)
        odom.pose.covariance[0] = 0.01   # x
        odom.pose.covariance[7] = 0.01   # y
        odom.pose.covariance[35] = 0.05  # theta
        
        self.odom_pub.publish(odom)
    
    def publish_transform(self, current_time):
        """Publish TF:  odom -> base_footprint"""
        t = TransformStamped()
        t.header.stamp = current_time.to_msg()
        t.header.frame_id = self.odom_frame
        t.child_frame_id = self.base_frame
        
        t.transform.translation. x = self.x
        t.transform.translation.y = self.y
        t.transform. translation.z = 0.0
        t.transform.rotation = self.yaw_to_quaternion(self.theta)
        
        self.tf_broadcaster.sendTransform(t)
    
    def publish_joint_states(self, current_time):
        """Publish wheel joint states for RViz"""
        joint_state = JointState()
        joint_state.header.stamp = current_time.to_msg()
        joint_state.name = ['left_wheel_joint', 'right_wheel_joint']
        
        # Wheel positions (integrate velocities)
        # This is just for visualization, not critical
        joint_state.position = [0.0, 0.0]  # Could integrate over time
        joint_state.velocity = [self.vx / self.wheel_radius, self.vx / self.wheel_radius]
        joint_state.effort = []
        
        self.joint_pub.publish(joint_state)
    
    def yaw_to_quaternion(self, yaw):
        """Convert yaw angle to quaternion"""
        q = Quaternion()
        q.x = 0.0
        q.y = 0.0
        q.z = math.sin(yaw / 2.0)
        q.w = math.cos(yaw / 2.0)
        return q
    
    def destroy_node(self):
        if self.serial_conn and self. serial_conn.is_open:
            self.serial_conn. close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = WheelOdometry()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally: 
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()