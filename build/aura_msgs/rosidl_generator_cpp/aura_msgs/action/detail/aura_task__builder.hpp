// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aura_msgs:action/AuraTask.idl
// generated code does not contain a copyright notice

#ifndef AURA_MSGS__ACTION__DETAIL__AURA_TASK__BUILDER_HPP_
#define AURA_MSGS__ACTION__DETAIL__AURA_TASK__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aura_msgs/action/detail/aura_task__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aura_msgs
{

namespace action
{

namespace builder
{

class Init_AuraTask_Goal_task_number
{
public:
  Init_AuraTask_Goal_task_number()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::aura_msgs::action::AuraTask_Goal task_number(::aura_msgs::action::AuraTask_Goal::_task_number_type arg)
  {
    msg_.task_number = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aura_msgs::action::AuraTask_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::aura_msgs::action::AuraTask_Goal>()
{
  return aura_msgs::action::builder::Init_AuraTask_Goal_task_number();
}

}  // namespace aura_msgs


namespace aura_msgs
{

namespace action
{

namespace builder
{

class Init_AuraTask_Result_success
{
public:
  Init_AuraTask_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::aura_msgs::action::AuraTask_Result success(::aura_msgs::action::AuraTask_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aura_msgs::action::AuraTask_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::aura_msgs::action::AuraTask_Result>()
{
  return aura_msgs::action::builder::Init_AuraTask_Result_success();
}

}  // namespace aura_msgs


namespace aura_msgs
{

namespace action
{

namespace builder
{

class Init_AuraTask_Feedback_percentage
{
public:
  Init_AuraTask_Feedback_percentage()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::aura_msgs::action::AuraTask_Feedback percentage(::aura_msgs::action::AuraTask_Feedback::_percentage_type arg)
  {
    msg_.percentage = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aura_msgs::action::AuraTask_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::aura_msgs::action::AuraTask_Feedback>()
{
  return aura_msgs::action::builder::Init_AuraTask_Feedback_percentage();
}

}  // namespace aura_msgs


namespace aura_msgs
{

namespace action
{

namespace builder
{

class Init_AuraTask_SendGoal_Request_goal
{
public:
  explicit Init_AuraTask_SendGoal_Request_goal(::aura_msgs::action::AuraTask_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::aura_msgs::action::AuraTask_SendGoal_Request goal(::aura_msgs::action::AuraTask_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aura_msgs::action::AuraTask_SendGoal_Request msg_;
};

class Init_AuraTask_SendGoal_Request_goal_id
{
public:
  Init_AuraTask_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AuraTask_SendGoal_Request_goal goal_id(::aura_msgs::action::AuraTask_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_AuraTask_SendGoal_Request_goal(msg_);
  }

private:
  ::aura_msgs::action::AuraTask_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::aura_msgs::action::AuraTask_SendGoal_Request>()
{
  return aura_msgs::action::builder::Init_AuraTask_SendGoal_Request_goal_id();
}

}  // namespace aura_msgs


namespace aura_msgs
{

namespace action
{

namespace builder
{

class Init_AuraTask_SendGoal_Response_stamp
{
public:
  explicit Init_AuraTask_SendGoal_Response_stamp(::aura_msgs::action::AuraTask_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::aura_msgs::action::AuraTask_SendGoal_Response stamp(::aura_msgs::action::AuraTask_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aura_msgs::action::AuraTask_SendGoal_Response msg_;
};

class Init_AuraTask_SendGoal_Response_accepted
{
public:
  Init_AuraTask_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AuraTask_SendGoal_Response_stamp accepted(::aura_msgs::action::AuraTask_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_AuraTask_SendGoal_Response_stamp(msg_);
  }

private:
  ::aura_msgs::action::AuraTask_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::aura_msgs::action::AuraTask_SendGoal_Response>()
{
  return aura_msgs::action::builder::Init_AuraTask_SendGoal_Response_accepted();
}

}  // namespace aura_msgs


namespace aura_msgs
{

namespace action
{

namespace builder
{

class Init_AuraTask_GetResult_Request_goal_id
{
public:
  Init_AuraTask_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::aura_msgs::action::AuraTask_GetResult_Request goal_id(::aura_msgs::action::AuraTask_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aura_msgs::action::AuraTask_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::aura_msgs::action::AuraTask_GetResult_Request>()
{
  return aura_msgs::action::builder::Init_AuraTask_GetResult_Request_goal_id();
}

}  // namespace aura_msgs


namespace aura_msgs
{

namespace action
{

namespace builder
{

class Init_AuraTask_GetResult_Response_result
{
public:
  explicit Init_AuraTask_GetResult_Response_result(::aura_msgs::action::AuraTask_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::aura_msgs::action::AuraTask_GetResult_Response result(::aura_msgs::action::AuraTask_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aura_msgs::action::AuraTask_GetResult_Response msg_;
};

class Init_AuraTask_GetResult_Response_status
{
public:
  Init_AuraTask_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AuraTask_GetResult_Response_result status(::aura_msgs::action::AuraTask_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_AuraTask_GetResult_Response_result(msg_);
  }

private:
  ::aura_msgs::action::AuraTask_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::aura_msgs::action::AuraTask_GetResult_Response>()
{
  return aura_msgs::action::builder::Init_AuraTask_GetResult_Response_status();
}

}  // namespace aura_msgs


namespace aura_msgs
{

namespace action
{

namespace builder
{

class Init_AuraTask_FeedbackMessage_feedback
{
public:
  explicit Init_AuraTask_FeedbackMessage_feedback(::aura_msgs::action::AuraTask_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::aura_msgs::action::AuraTask_FeedbackMessage feedback(::aura_msgs::action::AuraTask_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aura_msgs::action::AuraTask_FeedbackMessage msg_;
};

class Init_AuraTask_FeedbackMessage_goal_id
{
public:
  Init_AuraTask_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AuraTask_FeedbackMessage_feedback goal_id(::aura_msgs::action::AuraTask_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_AuraTask_FeedbackMessage_feedback(msg_);
  }

private:
  ::aura_msgs::action::AuraTask_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::aura_msgs::action::AuraTask_FeedbackMessage>()
{
  return aura_msgs::action::builder::Init_AuraTask_FeedbackMessage_goal_id();
}

}  // namespace aura_msgs

#endif  // AURA_MSGS__ACTION__DETAIL__AURA_TASK__BUILDER_HPP_
