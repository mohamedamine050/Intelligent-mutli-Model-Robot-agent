#!/usr/bin/env python3
"""
Launch robot with SLAM (mapping mode)
Use this to create a map of your environment
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
                    'bringup.launch. py'
                ])
            ]),
            launch_arguments={
                'use_slam': 'true',
                'use_nav': 'false',
                'use_rviz': 'true',
            }.items()
        )
    ])