#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """
    Launch stereo depth processing node
    """
    
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    return LaunchDescription([
        
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation time'
        ),
        
        Node(
            package='robot_sensors',
            executable='stereo_depth_node',
            name='stereo_depth',
            output='screen',
            parameters=[{
                'use_sim_time': use_sim_time,
                'baseline': 0.075,  # MEASURE the distance between your 2 ESP32-CAMs!  (meters)
                'focal_length': 500.0,  # From calibration (pixels)
                'min_disparity': 0,
                'num_disparities': 80,  # Must be divisible by 16
                'block_size': 15,
            }],
        ),
    ])