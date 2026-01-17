from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='robot_brain_bridge',
            executable='orion_bridge_node',
            name='orion_bridge_node',
            output='screen',
            parameters=[{}],
        )
    ])