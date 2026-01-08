#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range
from std_msgs.msg import Bool


class SafetyMux(Node):
    """
    Safety multiplexer: 
    - Subscribes to /cmd_vel (from Nav2/teleop)
    - Subscribes to /ultrasonic/front (Range)
    - Publishes to /cmd_vel_safe (to wheel_driver)
    - Stops robot if obstacle too close
    """
    
    def __init__(self):
        super().__init__('safety_mux')
        
        # Parameters
        self.declare_parameter('stop_distance', 0.15)   # meters (15 cm)
        self.declare_parameter('slow_distance', 0.30)   # meters (30 cm)
        self.declare_parameter('slow_factor', 0.3)      # Reduce speed to 30%
        
        self.stop_distance = self.get_parameter('stop_distance').value
        self.slow_distance = self.get_parameter('slow_distance').value
        self.slow_factor = self.get_parameter('slow_factor').value
        
        # State
        self. current_distance = 10.0  # meters (far away initially)
        self.desired_cmd = Twist()
        self.is_stopped = False
        
        # Subscribers
        self.cmd_sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )
        
        self.range_sub = self.create_subscription(
            Range,
            '/ultrasonic/front',
            self.ultrasonic_callback,
            10
        )
        
        # Publishers
        self. safe_cmd_pub = self.create_publisher(Twist, '/cmd_vel_safe', 10)
        self.stop_pub = self.create_publisher(Bool, '/safety/stop', 10)
        
        # Timer to publish safe commands (even if no new cmd_vel)
        self.create_timer(0.1, self.publish_safe_cmd)  # 10 Hz
        
        self. get_logger().info('Safety mux started')
    
    def cmd_vel_callback(self, msg):
        """Store desired velocity command"""
        self.desired_cmd = msg
    
    def ultrasonic_callback(self, msg):
        """Update current obstacle distance"""
        self.current_distance = msg.range
    
    def publish_safe_cmd(self):
        """
        Decide whether to forward, slow, or stop the command
        based on ultrasonic distance
        """
        safe_cmd = Twist()
        
        # Check if obstacle is too close
        if self.current_distance < self.stop_distance:
            # STOP:  obstacle very close
            safe_cmd.linear.x = 0.0
            safe_cmd.angular.z = 0.0
            
            if not self.is_stopped:
                self.get_logger().warn(f'EMERGENCY STOP!  Distance: {self.current_distance:. 2f}m')
                self.is_stopped = True
                self.stop_pub.publish(Bool(data=True))
        
        elif self.current_distance < self. slow_distance:
            # SLOW DOWN: obstacle approaching
            safe_cmd.linear. x = self.desired_cmd.linear.x * self.slow_factor
            safe_cmd.angular.z = self. desired_cmd.angular.z
            
            if self.is_stopped:
                self.get_logger().info('Obstacle cleared, resuming (slow)')
                self.is_stopped = False
                self.stop_pub.publish(Bool(data=False))
        
        else: 
            # NORMAL: forward command as-is
            safe_cmd = self.desired_cmd
            
            if self.is_stopped:
                self.get_logger().info('Obstacle cleared, resuming')
                self.is_stopped = False
                self.stop_pub.publish(Bool(data=False))
        
        # Publish safe command
        self. safe_cmd_pub.publish(safe_cmd)


def main(args=None):
    rclpy.init(args=args)
    node = SafetyMux()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node. destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()