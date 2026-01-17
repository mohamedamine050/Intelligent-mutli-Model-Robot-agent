#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    """
    Launch SLAM Toolbox in async mode

    Modes:
    - mapping: Create new map (default)
    - localization: Use existing map
    """

    # Arguments
    use_sim_time = LaunchConfiguration('use_sim_time')
    slam_mode = LaunchConfiguration('slam_mode')
    map_file = LaunchConfiguration('map_file')

    # Paths
    slam_params_file = PathJoinSubstitution([
        FindPackageShare('robot_slam'),
        'config',
        'slam_params.yaml'
    ])

    return LaunchDescription([

        # ========== Arguments ==========
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation time'
        ),

        DeclareLaunchArgument(
            'slam_mode',
            default_value='mapping',
            description='SLAM mode: mapping or localization'
        ),

        DeclareLaunchArgument(
            'map_file',
            default_value='',
            description='Path to map file for localization mode'
        ),

        # ========== SLAM Toolbox (Async Mapping) ==========
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[
                slam_params_file,
                {
                    'use_sim_time': use_sim_time,
                }
            ],
            condition=UnlessCondition(
                # Evaluate at runtime whether slam_mode == 'localization'
                PythonExpression(["'", slam_mode, "' == 'localization'"])
            )
        ),

        # ========== SLAM Toolbox (Localization) ==========
        Node(
            package='slam_toolbox',
            executable='localization_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[
                slam_params_file,
                {
                    'use_sim_time': use_sim_time,
                    'map_file_name': map_file,
                }
            ],
            condition=IfCondition(
                PythonExpression(["'", slam_mode, "' == 'localization'"])
            )
        ),
    ])