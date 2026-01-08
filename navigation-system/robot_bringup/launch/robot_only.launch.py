#!/usr/bin/env python3
"""
Launch ONLY the base robot (control + sensors, no SLAM/Nav)
Useful for testing and teleoperation
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
                'use_slam': 'false',
                'use_nav': 'false',
                'use_rviz': 'true',
            }.items()
        )
    ])