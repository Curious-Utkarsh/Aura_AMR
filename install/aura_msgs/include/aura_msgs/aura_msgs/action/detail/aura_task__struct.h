// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aura_msgs:action/AuraTask.idl
// generated code does not contain a copyright notice

#ifndef AURA_MSGS__ACTION__DETAIL__AURA_TASK__STRUCT_H_
#define AURA_MSGS__ACTION__DETAIL__AURA_TASK__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in action/AuraTask in the package aura_msgs.
typedef struct aura_msgs__action__AuraTask_Goal
{
  int32_t task_number;
} aura_msgs__action__AuraTask_Goal;

// Struct for a sequence of aura_msgs__action__AuraTask_Goal.
typedef struct aura_msgs__action__AuraTask_Goal__Sequence
{
  aura_msgs__action__AuraTask_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aura_msgs__action__AuraTask_Goal__Sequence;


// Constants defined in the message

/// Struct defined in action/AuraTask in the package aura_msgs.
typedef struct aura_msgs__action__AuraTask_Result
{
  bool success;
} aura_msgs__action__AuraTask_Result;

// Struct for a sequence of aura_msgs__action__AuraTask_Result.
typedef struct aura_msgs__action__AuraTask_Result__Sequence
{
  aura_msgs__action__AuraTask_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aura_msgs__action__AuraTask_Result__Sequence;


// Constants defined in the message

/// Struct defined in action/AuraTask in the package aura_msgs.
typedef struct aura_msgs__action__AuraTask_Feedback
{
  int32_t percentage;
} aura_msgs__action__AuraTask_Feedback;

// Struct for a sequence of aura_msgs__action__AuraTask_Feedback.
typedef struct aura_msgs__action__AuraTask_Feedback__Sequence
{
  aura_msgs__action__AuraTask_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aura_msgs__action__AuraTask_Feedback__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "aura_msgs/action/detail/aura_task__struct.h"

/// Struct defined in action/AuraTask in the package aura_msgs.
typedef struct aura_msgs__action__AuraTask_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  aura_msgs__action__AuraTask_Goal goal;
} aura_msgs__action__AuraTask_SendGoal_Request;

// Struct for a sequence of aura_msgs__action__AuraTask_SendGoal_Request.
typedef struct aura_msgs__action__AuraTask_SendGoal_Request__Sequence
{
  aura_msgs__action__AuraTask_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aura_msgs__action__AuraTask_SendGoal_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/AuraTask in the package aura_msgs.
typedef struct aura_msgs__action__AuraTask_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} aura_msgs__action__AuraTask_SendGoal_Response;

// Struct for a sequence of aura_msgs__action__AuraTask_SendGoal_Response.
typedef struct aura_msgs__action__AuraTask_SendGoal_Response__Sequence
{
  aura_msgs__action__AuraTask_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aura_msgs__action__AuraTask_SendGoal_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/AuraTask in the package aura_msgs.
typedef struct aura_msgs__action__AuraTask_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} aura_msgs__action__AuraTask_GetResult_Request;

// Struct for a sequence of aura_msgs__action__AuraTask_GetResult_Request.
typedef struct aura_msgs__action__AuraTask_GetResult_Request__Sequence
{
  aura_msgs__action__AuraTask_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aura_msgs__action__AuraTask_GetResult_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "aura_msgs/action/detail/aura_task__struct.h"

/// Struct defined in action/AuraTask in the package aura_msgs.
typedef struct aura_msgs__action__AuraTask_GetResult_Response
{
  int8_t status;
  aura_msgs__action__AuraTask_Result result;
} aura_msgs__action__AuraTask_GetResult_Response;

// Struct for a sequence of aura_msgs__action__AuraTask_GetResult_Response.
typedef struct aura_msgs__action__AuraTask_GetResult_Response__Sequence
{
  aura_msgs__action__AuraTask_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aura_msgs__action__AuraTask_GetResult_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "aura_msgs/action/detail/aura_task__struct.h"

/// Struct defined in action/AuraTask in the package aura_msgs.
typedef struct aura_msgs__action__AuraTask_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  aura_msgs__action__AuraTask_Feedback feedback;
} aura_msgs__action__AuraTask_FeedbackMessage;

// Struct for a sequence of aura_msgs__action__AuraTask_FeedbackMessage.
typedef struct aura_msgs__action__AuraTask_FeedbackMessage__Sequence
{
  aura_msgs__action__AuraTask_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aura_msgs__action__AuraTask_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AURA_MSGS__ACTION__DETAIL__AURA_TASK__STRUCT_H_
