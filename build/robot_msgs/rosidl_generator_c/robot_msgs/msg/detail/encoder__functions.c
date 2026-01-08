// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from robot_msgs:msg/Encoder.idl
// generated code does not contain a copyright notice
#include "robot_msgs/msg/detail/encoder__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"

bool
robot_msgs__msg__Encoder__init(robot_msgs__msg__Encoder * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    robot_msgs__msg__Encoder__fini(msg);
    return false;
  }
  // left_ticks
  // right_ticks
  return true;
}

void
robot_msgs__msg__Encoder__fini(robot_msgs__msg__Encoder * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // left_ticks
  // right_ticks
}

bool
robot_msgs__msg__Encoder__are_equal(const robot_msgs__msg__Encoder * lhs, const robot_msgs__msg__Encoder * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // left_ticks
  if (lhs->left_ticks != rhs->left_ticks) {
    return false;
  }
  // right_ticks
  if (lhs->right_ticks != rhs->right_ticks) {
    return false;
  }
  return true;
}

bool
robot_msgs__msg__Encoder__copy(
  const robot_msgs__msg__Encoder * input,
  robot_msgs__msg__Encoder * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // left_ticks
  output->left_ticks = input->left_ticks;
  // right_ticks
  output->right_ticks = input->right_ticks;
  return true;
}

robot_msgs__msg__Encoder *
robot_msgs__msg__Encoder__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robot_msgs__msg__Encoder * msg = (robot_msgs__msg__Encoder *)allocator.allocate(sizeof(robot_msgs__msg__Encoder), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(robot_msgs__msg__Encoder));
  bool success = robot_msgs__msg__Encoder__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
robot_msgs__msg__Encoder__destroy(robot_msgs__msg__Encoder * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    robot_msgs__msg__Encoder__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
robot_msgs__msg__Encoder__Sequence__init(robot_msgs__msg__Encoder__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robot_msgs__msg__Encoder * data = NULL;

  if (size) {
    data = (robot_msgs__msg__Encoder *)allocator.zero_allocate(size, sizeof(robot_msgs__msg__Encoder), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = robot_msgs__msg__Encoder__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        robot_msgs__msg__Encoder__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
robot_msgs__msg__Encoder__Sequence__fini(robot_msgs__msg__Encoder__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      robot_msgs__msg__Encoder__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

robot_msgs__msg__Encoder__Sequence *
robot_msgs__msg__Encoder__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robot_msgs__msg__Encoder__Sequence * array = (robot_msgs__msg__Encoder__Sequence *)allocator.allocate(sizeof(robot_msgs__msg__Encoder__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = robot_msgs__msg__Encoder__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
robot_msgs__msg__Encoder__Sequence__destroy(robot_msgs__msg__Encoder__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    robot_msgs__msg__Encoder__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
robot_msgs__msg__Encoder__Sequence__are_equal(const robot_msgs__msg__Encoder__Sequence * lhs, const robot_msgs__msg__Encoder__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!robot_msgs__msg__Encoder__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
robot_msgs__msg__Encoder__Sequence__copy(
  const robot_msgs__msg__Encoder__Sequence * input,
  robot_msgs__msg__Encoder__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(robot_msgs__msg__Encoder);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    robot_msgs__msg__Encoder * data =
      (robot_msgs__msg__Encoder *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!robot_msgs__msg__Encoder__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          robot_msgs__msg__Encoder__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!robot_msgs__msg__Encoder__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
