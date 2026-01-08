#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    config_file = PathJoinSubstitution([
        FindPackageShare('robot_sensors'),
        'config',
        'sensors_params.yaml'
    ])
    
    return LaunchDescription([
        
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation time'
        ),
        
        Node(
            package='robot_sensors',
            executable='ultrasonic_node',
            name='ultrasonic_node',
            output='screen',
            parameters=[config_file, {'use_sim_time': use_sim_time}],
        ),
    ])