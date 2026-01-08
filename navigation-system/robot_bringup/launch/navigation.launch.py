#!/usr/bin/env python3
"""
Launch robot with navigation (using pre-built map)
Requires a map file created with SLAM
"""

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    
    map_file = LaunchConfiguration('map_file')
    
    default_map = PathJoinSubstitution([
        FindPackageShare('robot_slam'),
        'maps',
        'my_map.yaml'
    ])
    
    return LaunchDescription([
        
        DeclareLaunchArgument(
            'map_file',
            default_value=default_map,
            description='Path to map file'
        ),
        
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('robot_bringup'),
                    'launch',
                    'bringup. launch.py'
                ])
            ]),
            launch_arguments={
                'use_slam':  'false',
                'use_nav':  'true',
                'map_file': map_file,
                'use_rviz': 'true',
            }.items()
        )
    ])