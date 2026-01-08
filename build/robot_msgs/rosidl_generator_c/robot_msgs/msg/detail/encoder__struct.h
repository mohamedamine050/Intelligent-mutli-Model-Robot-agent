// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from robot_msgs:msg/Encoder.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_MSGS__MSG__DETAIL__ENCODER__STRUCT_H_
#define ROBOT_MSGS__MSG__DETAIL__ENCODER__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"

/// Struct defined in msg/Encoder in the package robot_msgs.
/**
  * Encoder ticks from Arduino
  * These are incremental ticks since last message
 */
typedef struct robot_msgs__msg__Encoder
{
  std_msgs__msg__Header header;
  /// Left wheel encoder ticks
  int32_t left_ticks;
  /// Right wheel encoder ticks
  int32_t right_ticks;
} robot_msgs__msg__Encoder;

// Struct for a sequence of robot_msgs__msg__Encoder.
typedef struct robot_msgs__msg__Encoder__Sequence
{
  robot_msgs__msg__Encoder * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robot_msgs__msg__Encoder__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROBOT_MSGS__MSG__DETAIL__ENCODER__STRUCT_H_
