#!/usr/bin/env python3

from launch import LaunchDescription
from launch. actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """
    Launch 2 ESP32-CAM nodes (left and right)
    
    IMPORTANT: Configure your ESP32-CAM IP addresses!
    """
    
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    # CHANGE THESE TO YOUR ESP32-CAM IP ADDRESSES! 
    left_camera_ip = '192.168.1.100'
    right_camera_ip = '192.168.1.101'
    
    return LaunchDescription([
        
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation time'
        ),
        
        # Left camera
        Node(
            package='robot_sensors',
            executable='esp32_cam_node',
            name='esp32_cam_left',
            output='screen',
            parameters=[{
                'use_sim_time': use_sim_time,
                'camera_name': 'left',
                'camera_ip': left_camera_ip,
                'stream_port': 81,
                'frame_id': 'camera_left_frame',
                'publish_rate': 30.0,
                'image_width': 640,
                'image_height':  480,
            }],
        ),
        
        # Right camera
        Node(
            package='robot_sensors',
            executable='esp32_cam_node',
            name='esp32_cam_right',
            output='screen',
            parameters=[{
                'use_sim_time': use_sim_time,
                'camera_name': 'right',
                'camera_ip': right_camera_ip,
                'stream_port': 81,
                'frame_id': 'camera_right_frame',
                'publish_rate': 30.0,
                'image_width':  640,
                'image_height': 480,
            }],
        ),
    ])