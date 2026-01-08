#!/usr/bin/env python3
"""
R2D2 Robot Master Bringup Launch File

This is the MAIN launch file that orchestrates the entire robot system. 

Usage examples:
  # Basic:  control + sensors only
  ros2 launch robot_bringup bringup.launch.py

  # With SLAM (mapping)
  ros2 launch robot_bringup bringup.launch.py use_slam:=true

  # With Navigation (pre-built map)
  ros2 launch robot_bringup bringup.launch.py use_nav:=true map_file:=/path/to/map.yaml

  # Full autonomous (SLAM + Nav2)
  ros2 launch robot_bringup bringup.launch.py use_slam:=true use_nav:=true

  # With RViz
  ros2 launch robot_bringup bringup.launch.py use_rviz:=true
"""

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    GroupAction,
    LogInfo
)
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    
    # ========================================
    # Launch Configuration Variables
    # ========================================
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_rviz = LaunchConfiguration('use_rviz')
    use_camera = LaunchConfiguration('use_camera')
    use_ultrasonic = LaunchConfiguration('use_ultrasonic')
    use_slam = LaunchConfiguration('use_slam')
    use_nav = LaunchConfiguration('use_nav')
    map_file = LaunchConfiguration('map_file')
    
    # ========================================
    # Default Paths
    # ========================================
    default_rviz_config = PathJoinSubstitution([
        FindPackageShare('robot_bringup'),
        'config',
        'robot.rviz'
    ])
    
    default_map_file = PathJoinSubstitution([
        FindPackageShare('robot_slam'),
        'maps',
        'my_map.yaml'
    ])
    
    # ========================================
    # Declare Launch Arguments
    # ========================================
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )
    
    declare_use_rviz = DeclareLaunchArgument(
        'use_rviz',
        default_value='true',
        description='Launch RViz for visualization'
    )
    
    declare_use_camera = DeclareLaunchArgument(
        'use_camera',
        default_value='true',
        description='Launch stereo camera (ESP32-CAM) and depth processing'
    )
    
    declare_use_ultrasonic = DeclareLaunchArgument(
        'use_ultrasonic',
        default_value='true',
        description='Launch ultrasonic sensor node'
    )
    
    declare_use_slam = DeclareLaunchArgument(
        'use_slam',
        default_value='false',
        description='Launch SLAM (mapping mode). If false and use_nav=true, localization mode is used.'
    )
    
    declare_use_nav = DeclareLaunchArgument(
        'use_nav',
        default_value='false',
        description='Launch Nav2 navigation stack'
    )
    
    declare_map_file = DeclareLaunchArgument(
        'map_file',
        default_value=default_map_file,
        description='Path to map YAML file (used when use_nav=true and use_slam=false)'
    )
    
    # ========================================
    # Startup Info
    # ========================================
    startup_info = LogInfo(
        msg=[
            '\n',
            '========================================\n',
            '  R2D2 Robot Bringup\n',
            '========================================\n',
            'use_sim_time: ', use_sim_time, '\n',
            'use_rviz: ', use_rviz, '\n',
            'use_camera: ', use_camera, '\n',
            'use_ultrasonic: ', use_ultrasonic, '\n',
            'use_slam: ', use_slam, '\n',
            'use_nav: ', use_nav, '\n',
            '========================================\n'
        ]
    )
    
    # ========================================
    # 1. Robot Description (URDF, TF)
    # ========================================
    robot_description = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('robot_description'),
                'launch',
                'description.launch.py'
            ])
        ]),
        launch_arguments={
            'use_sim_time': use_sim_time,
        }.items()
    )
    
    # ========================================
    # 2. Robot Control (motors, odometry, safety)
    # ========================================
    robot_control = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('robot_control'),
                'launch',
                'control.launch.py'
            ])
        ]),
        launch_arguments={
            'use_sim_time': use_sim_time,
        }.items()
    )
    
    # ========================================
    # 3.  Sensors
    # ========================================
    
    # 3.1 Ultrasonic sensor
    ultrasonic = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('robot_sensors'),
                'launch',
                'ultrasonic.launch.py'
            ])
        ]),
        launch_arguments={
            'use_sim_time': use_sim_time,
        }.items(),
        condition=IfCondition(use_ultrasonic)
    )
    
    # 3.2 Stereo cameras (ESP32-CAM)
    stereo_cameras = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('robot_sensors'),
                'launch',
                'esp32_cameras.launch.py'
            ])
        ]),
        launch_arguments={
            'use_sim_time': use_sim_time,
        }.items(),
        condition=IfCondition(use_camera)
    )
    
    # 3.3 Stereo depth processing
    stereo_depth = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('robot_sensors'),
                'launch',
                'stereo_depth.launch.py'
            ])
        ]),
        launch_arguments={
            'use_sim_time': use_sim_time,
        }.items(),
        condition=IfCondition(use_camera)
    )
    
    # 3.4 Depth to LaserScan conversion
    depth_to_scan = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('robot_sensors'),
                'launch',
                'depth_to_scan.launch.py'
            ])
        ]),
        launch_arguments={
            'use_sim_time': use_sim_time,
        }.items(),
        condition=IfCondition(use_camera)
    )
    
    # ========================================
    # 4. SLAM (mapping)
    # ========================================
    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('robot_slam'),
                'launch',
                'slam.launch.py'
            ])
        ]),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'slam_mode': 'mapping',
        }.items(),
        condition=IfCondition(use_slam)
    )
    
    # ========================================
    # 5. Navigation (Nav2)
    # ========================================
    navigation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('robot_navigation'),
                'launch',
                'navigation.launch. py'
            ])
        ]),
        launch_arguments={
            'use_sim_time':  use_sim_time,
            'use_slam': use_slam,
            'map_file': map_file,
        }.items(),
        condition=IfCondition(use_nav)
    )
    
    # ========================================
    # 6. RViz (Visualization)
    # ========================================
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', default_rviz_config],
        parameters=[{'use_sim_time':  use_sim_time}],
        condition=IfCondition(use_rviz)
    )
    
    # ========================================
    # Launch Description
    # ========================================
    return LaunchDescription([
        # Arguments
        declare_use_sim_time,
        declare_use_rviz,
        declare_use_camera,
        declare_use_ultrasonic,
        declare_use_slam,
        declare_use_nav,
        declare_map_file,
        
        # Info
        startup_info,
        
        # Core components (always launched)
        robot_description,
        robot_control,
        
        # Optional sensors
        ultrasonic,
        stereo_cameras,
        stereo_depth,
        depth_to_scan,
        
        # Optional SLAM
        slam,
        
        # Optional Navigation
        navigation,
        
        # Optional RViz
        rviz,
    ])