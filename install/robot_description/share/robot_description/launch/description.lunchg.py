#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    
    # Get package directory
    pkg_robot_description = get_package_share_directory('robot_description')
    
    # Path to URDF file
    urdf_file = os.path.join(pkg_robot_description, 'urdf', 'robot.urdf.xacro')
    
    # Declare arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )
    
    # Process XACRO file to URDF
    robot_description_content = ParameterValue(
        Command(['xacro ', urdf_file]),
        value_type=str
    )
    
    # Robot State Publisher - publishes robot TF tree
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_content,
            'use_sim_time': use_sim_time
        }]
    )
    
    # Joint State Publisher - publishes joint states (for non-simulated joints)
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time
        }]
    )
    
    # RViz2 - visualization
    rviz_config_file = os.path.join(pkg_robot_description, 'rviz', 'robot_view.rviz')
    
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file] if os.path.exists(rviz_config_file) else [],
        parameters=[{
            'use_sim_time': use_sim_time
        }]
    )
    
    return LaunchDescription([
        use_sim_time_arg,
        robot_state_publisher_node,
        joint_state_publisher_node,
        rviz_node
    ])