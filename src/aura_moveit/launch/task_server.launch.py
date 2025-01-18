import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # Declare arguments for simulation time configuration
    is_sim_arg = DeclareLaunchArgument(
        "is_sim",
        default_value="True",
        description="Use simulation time if true"
    )

    # Launch configurations
    is_sim = LaunchConfiguration("is_sim")

    # Configure MoveIt settings
    moveit_config = (
        MoveItConfigsBuilder("aura", package_name="aura_moveit")
        .robot_description(file_path=os.path.join(
            get_package_share_directory("aura_description"),
            "urdf",
            "aura.urdf.xacro"
            )
        )
        .robot_description_semantic(file_path=os.path.join(
            get_package_share_directory("aura_moveit"),
            "config",
            "aura.srdf"
            )
        )
        .trajectory_execution(file_path=os.path.join(
            get_package_share_directory("aura_moveit"),
            "config",
            "moveit_controllers.yaml"
            )
        )
        .moveit_cpp(file_path=os.path.join(
            get_package_share_directory("aura_moveit"),
            "config",
            "planning_python_api.yaml"
            )
        )
        .to_moveit_configs()
    )

    # Task server node
    task_server_node = Node(
        package="aura_moveit",
        executable="task_server",
        output="screen",
        parameters=[
            moveit_config.to_dict(),  # Pass MoveIt configuration as parameters
            {"use_sim_time": is_sim}  # Simulation time configuration
        ]
    )

    # Return the launch description
    return LaunchDescription([
        is_sim_arg,
        task_server_node
    ])
