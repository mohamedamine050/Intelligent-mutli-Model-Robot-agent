// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_msgs:msg/WheelCommand.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_MSGS__MSG__DETAIL__WHEEL_COMMAND__BUILDER_HPP_
#define ROBOT_MSGS__MSG__DETAIL__WHEEL_COMMAND__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_msgs/msg/detail/wheel_command__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_msgs
{

namespace msg
{

namespace builder
{

class Init_WheelCommand_right_velocity
{
public:
  explicit Init_WheelCommand_right_velocity(::robot_msgs::msg::WheelCommand & msg)
  : msg_(msg)
  {}
  ::robot_msgs::msg::WheelCommand right_velocity(::robot_msgs::msg::WheelCommand::_right_velocity_type arg)
  {
    msg_.right_velocity = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_msgs::msg::WheelCommand msg_;
};

class Init_WheelCommand_left_velocity
{
public:
  Init_WheelCommand_left_velocity()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_WheelCommand_right_velocity left_velocity(::robot_msgs::msg::WheelCommand::_left_velocity_type arg)
  {
    msg_.left_velocity = std::move(arg);
    return Init_WheelCommand_right_velocity(msg_);
  }

private:
  ::robot_msgs::msg::WheelCommand msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_msgs::msg::WheelCommand>()
{
  return robot_msgs::msg::builder::Init_WheelCommand_left_velocity();
}

}  // namespace robot_msgs

#endif  // ROBOT_MSGS__MSG__DETAIL__WHEEL_COMMAND__BUILDER_HPP_
