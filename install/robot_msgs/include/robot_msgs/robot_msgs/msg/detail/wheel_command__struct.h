// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from robot_msgs:msg/WheelCommand.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_MSGS__MSG__DETAIL__WHEEL_COMMAND__STRUCT_H_
#define ROBOT_MSGS__MSG__DETAIL__WHEEL_COMMAND__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/WheelCommand in the package robot_msgs.
/**
  * Command velocities for left and right wheels
  * Units: rad/s (angular velocity) or m/s (linear velocity)
 */
typedef struct robot_msgs__msg__WheelCommand
{
  float left_velocity;
  float right_velocity;
} robot_msgs__msg__WheelCommand;

// Struct for a sequence of robot_msgs__msg__WheelCommand.
typedef struct robot_msgs__msg__WheelCommand__Sequence
{
  robot_msgs__msg__WheelCommand * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robot_msgs__msg__WheelCommand__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROBOT_MSGS__MSG__DETAIL__WHEEL_COMMAND__STRUCT_H_
