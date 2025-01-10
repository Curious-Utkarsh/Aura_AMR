import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        remappings=[
            ('/joint_states', '/joint_commands'),
        ]
    )

    slider_control_node = Node(
        package='aura_controller',
        executable='slider_arm.py'
    )

    return LaunchDescription(
        [
            joint_state_publisher_gui_node,
            slider_control_node,
        ]
    )
