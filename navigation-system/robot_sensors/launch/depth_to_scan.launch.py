#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """
    Converts depth image to LaserScan (/scan)
    Uses depthimage_to_laserscan package
    
    Install:  sudo apt install ros-humble-depthimage-to-laserscan
    """
    
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    return LaunchDescription([
        
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation time'
        ),
        
        Node(
            package='depthimage_to_laserscan',
            executable='depthimage_to_laserscan_node',
            name='depthimage_to_laserscan',
            output='screen',
            parameters=[{
                'use_sim_time': use_sim_time,
            }],
            remappings=[
                # Map depth image topic (from OAK-D) to input
                ('depth', '/stereo/depth'),
                ('depth_camera_info', '/stereo/depth/camera_info'),
                # Output scan topic
                ('scan', '/scan'),
            ],
        ),
    ])