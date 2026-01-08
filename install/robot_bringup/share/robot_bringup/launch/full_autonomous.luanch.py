#!/usr/bin/env python3
"""
Launch robot in FULL AUTONOMOUS mode
- SLAM for mapping
- Nav2 for navigation
- RViz for monitoring

This is the most advanced mode! 
"""

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('robot_bringup'),
                    'launch',
                    'bringup.launch.py'
                ])
            ]),
            launch_arguments={
                'use_slam': 'true',
                'use_nav': 'true',
                'use_rviz': 'true',
            }.items()
        )
    ])