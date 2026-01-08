// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from robot_msgs:msg/WheelCommand.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_MSGS__MSG__DETAIL__WHEEL_COMMAND__STRUCT_HPP_
#define ROBOT_MSGS__MSG__DETAIL__WHEEL_COMMAND__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__robot_msgs__msg__WheelCommand __attribute__((deprecated))
#else
# define DEPRECATED__robot_msgs__msg__WheelCommand __declspec(deprecated)
#endif

namespace robot_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct WheelCommand_
{
  using Type = WheelCommand_<ContainerAllocator>;

  explicit WheelCommand_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->left_velocity = 0.0f;
      this->right_velocity = 0.0f;
    }
  }

  explicit WheelCommand_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->left_velocity = 0.0f;
      this->right_velocity = 0.0f;
    }
  }

  // field types and members
  using _left_velocity_type =
    float;
  _left_velocity_type left_velocity;
  using _right_velocity_type =
    float;
  _right_velocity_type right_velocity;

  // setters for named parameter idiom
  Type & set__left_velocity(
    const float & _arg)
  {
    this->left_velocity = _arg;
    return *this;
  }
  Type & set__right_velocity(
    const float & _arg)
  {
    this->right_velocity = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robot_msgs::msg::WheelCommand_<ContainerAllocator> *;
  using ConstRawPtr =
    const robot_msgs::msg::WheelCommand_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robot_msgs::msg::WheelCommand_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robot_msgs::msg::WheelCommand_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robot_msgs::msg::WheelCommand_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robot_msgs::msg::WheelCommand_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robot_msgs::msg::WheelCommand_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robot_msgs::msg::WheelCommand_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robot_msgs::msg::WheelCommand_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robot_msgs::msg::WheelCommand_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robot_msgs__msg__WheelCommand
    std::shared_ptr<robot_msgs::msg::WheelCommand_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robot_msgs__msg__WheelCommand
    std::shared_ptr<robot_msgs::msg::WheelCommand_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const WheelCommand_ & other) const
  {
    if (this->left_velocity != other.left_velocity) {
      return false;
    }
    if (this->right_velocity != other.right_velocity) {
      return false;
    }
    return true;
  }
  bool operator!=(const WheelCommand_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct WheelCommand_

// alias to use template instance with default allocator
using WheelCommand =
  robot_msgs::msg::WheelCommand_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace robot_msgs

#endif  // ROBOT_MSGS__MSG__DETAIL__WHEEL_COMMAND__STRUCT_HPP_
