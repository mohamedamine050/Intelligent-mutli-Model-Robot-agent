#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, GroupAction
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch. conditions import IfCondition
from launch_ros.actions import Node, SetRemap
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os


def generate_launch_description():
    """
    Launch Nav2 navigation stack
    
    Modes:
    - With SLAM: map is generated live (use_slam: =true)
    - With pre-built map: localization only (use_slam:=false, provide map_file)
    """
    
    # Arguments
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_slam = LaunchConfiguration('use_slam')
    map_file = LaunchConfiguration('map_file')
    params_file = LaunchConfiguration('params_file')
    autostart = LaunchConfiguration('autostart')
    use_composition = LaunchConfiguration('use_composition')
    use_respawn = LaunchConfiguration('use_respawn')
    
    # Paths
    nav2_bringup_dir = FindPackageShare('nav2_bringup').find('nav2_bringup')
    
    default_params_file = PathJoinSubstitution([
        FindPackageShare('robot_navigation'),
        'config',
        'nav2_params.yaml'
    ])
    
    default_map_file = PathJoinSubstitution([
        FindPackageShare('robot_slam'),
        'maps',
        'my_map.yaml'
    ])
    
    return LaunchDescription([
        
        # ========== Arguments ==========
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation time'
        ),
        
        DeclareLaunchArgument(
            'use_slam',
            default_value='false',
            description='Use SLAM for mapping (true) or pre-built map (false)'
        ),
        
        DeclareLaunchArgument(
            'map_file',
            default_value=default_map_file,
            description='Path to map YAML file (only if use_slam: =false)'
        ),
        
        DeclareLaunchArgument(
            'params_file',
            default_value=default_params_file,
            description='Path to Nav2 parameters YAML file'
        ),
        
        DeclareLaunchArgument(
            'autostart',
            default_value='true',
            description='Automatically startup the nav2 stack'
        ),
        
        DeclareLaunchArgument(
            'use_composition',
            default_value='False',
            description='Use composed bringup if True'
        ),
        
        DeclareLaunchArgument(
            'use_respawn',
            default_value='False',
            description='Whether to respawn if a node crashes'
        ),
        
        # ========== Include Nav2 Bringup ==========
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav2_bringup_dir, 'launch', 'navigation_launch.py')
            ),
            launch_arguments={
                'use_sim_time': use_sim_time,
                'params_file': params_file,
                'autostart': autostart,
                'use_composition': use_composition,
                'use_respawn': use_respawn,
            }.items()
        ),
        
        # ========== Map Server (only if not using SLAM) ==========
        GroupAction(
            condition=IfCondition(use_slam),
            actions=[
                Node(
                    package='nav2_map_server',
                    executable='map_server',
                    name='map_server',
                    output='screen',
                    parameters=[
                        {'use_sim_time': use_sim_time},
                        {'yaml_filename': map_file}
                    ],
                ),
                
                Node(
                    package='nav2_lifecycle_manager',
                    executable='lifecycle_manager',
                    name='lifecycle_manager_map_server',
                    output='screen',
                    parameters=[
                        {'use_sim_time': use_sim_time},
                        {'autostart': autostart},
                        {'node_names': ['map_server']}
                    ]
                ),
            ]
        ),
    ])