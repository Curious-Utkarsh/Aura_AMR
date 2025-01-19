#include <rclcpp/rclcpp.hpp>
#include <rclcpp_action/rclcpp_action.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include "aura_msgs/action/aura_task.hpp"

#include <memory>
#include <thread>
#include <vector>

using namespace std::placeholders;

namespace aura_moveit
{
class TaskServer : public rclcpp::Node
{
public:
  explicit TaskServer(const rclcpp::NodeOptions& options = rclcpp::NodeOptions())
    : Node("task_server", options)
  {
    RCLCPP_INFO(get_logger(), "Starting the Server");
    action_server_ = rclcpp_action::create_server<aura_msgs::action::AuraTask>(
        this, "task_server", 
        std::bind(&TaskServer::goalCallback, this, _1, _2),
        std::bind(&TaskServer::cancelCallback, this, _1),
        std::bind(&TaskServer::acceptedCallback, this, _1));
  }

private:
  rclcpp_action::Server<aura_msgs::action::AuraTask>::SharedPtr action_server_;
  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> arm_move_group, gripper_move_group;
  std::vector<double> arm_joint_goal, gripper_joint_goal;

  rclcpp_action::GoalResponse goalCallback(
      const rclcpp_action::GoalUUID& uuid,
      std::shared_ptr<const aura_msgs::action::AuraTask::Goal> goal)
  {
    RCLCPP_INFO(get_logger(), "Received goal request with id %d", goal->task_number);
    (void)uuid;
    return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
  }

  rclcpp_action::CancelResponse cancelCallback(
      const std::shared_ptr<rclcpp_action::ServerGoalHandle<aura_msgs::action::AuraTask>> goal_handle)
  {
    (void)goal_handle;
    RCLCPP_INFO(get_logger(), "Received request to cancel goal");
    auto arm_move_group = moveit::planning_interface::MoveGroupInterface(shared_from_this(), "arm");
    auto gripper_move_group = moveit::planning_interface::MoveGroupInterface(shared_from_this(), "gripper");
    arm_move_group.stop();
    gripper_move_group.stop();
    return rclcpp_action::CancelResponse::ACCEPT;
  }

  void acceptedCallback(
      const std::shared_ptr<rclcpp_action::ServerGoalHandle<aura_msgs::action::AuraTask>> goal_handle)
  {
    std::thread{std::bind(&TaskServer::execute, this, _1), goal_handle}.detach();
  }

  void execute(const std::shared_ptr<rclcpp_action::ServerGoalHandle<aura_msgs::action::AuraTask>> goal_handle)
  {
    RCLCPP_INFO(get_logger(), "Executing goal");
    auto result = std::make_shared<aura_msgs::action::AuraTask::Result>();

    if (!arm_move_group)
    {
      arm_move_group = std::make_shared<moveit::planning_interface::MoveGroupInterface>(shared_from_this(), "arm");
    }
    if (!gripper_move_group)
    {
      gripper_move_group = std::make_shared<moveit::planning_interface::MoveGroupInterface>(shared_from_this(), "gripper");
    }

    if (goal_handle->get_goal()->task_number == 0)
    {
      arm_joint_goal = {0.0, 1.0, 1.257, -0.653, 0.0};
      gripper_joint_goal = {-0.550, 0.550};
    }
    else if (goal_handle->get_goal()->task_number == 1)
    {
      arm_joint_goal = {0.0, -0.0, -1.0, 0.0, 0.0};
      gripper_joint_goal = {-0.550, 0.550};
    }
    else if (goal_handle->get_goal()->task_number == 2)
    {
      arm_joint_goal = {0.0, -0.110, 1.284, 0.382, 0.059};
      gripper_joint_goal = {-0.0, 0.0};
    }
    else
    {
      RCLCPP_ERROR(get_logger(), "Invalid Task Number");
      return;
    }

    arm_move_group->setStartState(*arm_move_group->getCurrentState());
    gripper_move_group->setStartState(*gripper_move_group->getCurrentState());

    bool arm_within_bounds = arm_move_group->setJointValueTarget(arm_joint_goal);
    bool gripper_within_bounds = gripper_move_group->setJointValueTarget(gripper_joint_goal);
    if (!arm_within_bounds || !gripper_within_bounds)
    {
      RCLCPP_WARN(get_logger(), "Target joint position(s) were outside of limits, but we will plan and clamp to the limits");
      return;
    }

    moveit::planning_interface::MoveGroupInterface::Plan arm_plan;
    moveit::planning_interface::MoveGroupInterface::Plan gripper_plan;
    bool arm_plan_success = (arm_move_group->plan(arm_plan) == moveit::core::MoveItErrorCode::SUCCESS);
    bool gripper_plan_success = (gripper_move_group->plan(gripper_plan) == moveit::core::MoveItErrorCode::SUCCESS);

    if (arm_plan_success && gripper_plan_success)
    {
      RCLCPP_INFO(get_logger(), "Planner SUCCEED, moving the arm and the gripper");
      arm_move_group->move();
      gripper_move_group->move();
    }
    else
    {
      RCLCPP_ERROR(get_logger(), "One or more planners failed!");
      return;
    }

    result->success = true;
    goal_handle->succeed(result);
    RCLCPP_INFO(get_logger(), "Goal succeeded");
  }
};
}  // namespace aura_moveit

int main(int argc, char** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<aura_moveit::TaskServer>());
  rclcpp::shutdown();
  return 0;
}
