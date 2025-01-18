cmake_minimum_required(VERSION 3.5)
project(aura_moveit)

# Required dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(rclcpp_components REQUIRED)
find_package(aura_msgs REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)

# Add the executable for the task server
add_executable(task_server src/task_server.cpp)

# Link the executable with required libraries
ament_target_dependencies(task_server
  rclcpp
  rclcpp_action
  rclcpp_components
  aura_msgs
  std_msgs
  moveit_ros_planning_interface
)

# Install the task server executable
install(
  TARGETS task_server
  DESTINATION lib/${PROJECT_NAME}
)

# Install additional files like launch and config
install(
  DIRECTORY launch config
  DESTINATION share/${PROJECT_NAME}
)

# Add testing if enabled
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

# Finalize the package
ament_package()
