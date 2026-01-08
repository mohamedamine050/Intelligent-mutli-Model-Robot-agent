#!/usr/bin/env python3

from launch import LaunchDescription
from launch. actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    
    # Parameters
    use_sim_time = LaunchConfiguration('use_sim_time')
    config_file = PathJoinSubstitution([
        FindPackageShare('robot_control'),
        'config',
        'control_params.yaml'
    ])
    
    return LaunchDescription([
        
        # Argument
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation time'
        ),
        
        # Wheel driver node
        Node(
            package='robot_control',
            executable='wheel_driver',
            name='wheel_driver',
            output='screen',
            parameters=[config_file, {'use_sim_time': use_sim_time}],
        ),
        
        # Wheel odometry node
        Node(
            package='robot_control',
            executable='wheel_odom',
            name='wheel_odom',
            output='screen',
            parameters=[config_file, {'use_sim_time':  use_sim_time}],
        ),
        
        # Safety mux node
        Node(
            package='robot_control',
            executable='safety_mux',
            name='safety_mux',
            output='screen',
            parameters=[config_file, {'use_sim_time': use_sim_time}],
        ),
    ])