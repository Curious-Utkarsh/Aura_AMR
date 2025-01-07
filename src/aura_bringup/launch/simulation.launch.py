import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

# Path to SLAM configuration
slam_rviz_config_path = os.path.join(
    get_package_share_directory('aura_mapping'),
    'rviz',
    'slam.rviz'
)


def generate_launch_description():
    gazebo = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("aura_description"),
            "launch",
            "gazebo.launch.py"
        ),
    )
    
    controller = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("aura_controller"),
            "launch",
            "controller.launch.py"
        ),
    )

    # rviz = IncludeLaunchDescription(
    #     os.path.join(
    #         get_package_share_directory("aura_description"),
    #         "launch",
    #         "display.launch.py"
    #     ),
    # )
    
    rviz = Node(
        package='rviz2', 
        executable='rviz2', 
        name='rviz', 
        output='screen',
        arguments=['-d', slam_rviz_config_path]  
    )
    
    joystick = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("aura_controller"),
            "launch",
            "joystick.launch.py"
        ),
        launch_arguments={
            "use_sim_time": "True"
        }.items()
    )
    
    return LaunchDescription([
        gazebo,
        controller,
        rviz,
        joystick,
    ])