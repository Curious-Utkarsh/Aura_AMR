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

# Path to Localization configuration
localization_rviz_config_path = os.path.join(
    get_package_share_directory('aura_localization'),
    'rviz',
    'global_localization.rviz'
)


def generate_launch_description():
    gazebo = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("aura_description"),
            "launch",
            "gazebo.launch.py"
        ),
    )

    rviz = Node(
        package='rviz2', 
        executable='rviz2', 
        name='rviz', 
        output='screen',
        # arguments=['-d', slam_rviz_config_path]  #For Mapping
        arguments=['-d', localization_rviz_config_path] #For Localization
    )
    
    controller = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("aura_controller"),
            "launch",
            "controller.launch.py"
        ),
    )

    global_localization = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("aura_localization"),
            "launch", 
            "global_localization.launch.py"
            ),
        )
    
    navigation = IncludeLaunchDescription(
        os.path.join(get_package_share_directory("aura_navigation"),
                      "launch",
                      "navigation.launch.py"
                      ),
    )

    pose_estimator = Node(
        package="aura_navigation",
        executable="pose_estimator.py",
        name="pose_estimator",
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
        rviz,
        controller,
        global_localization,
        navigation,
        pose_estimator,
        joystick,
    ])