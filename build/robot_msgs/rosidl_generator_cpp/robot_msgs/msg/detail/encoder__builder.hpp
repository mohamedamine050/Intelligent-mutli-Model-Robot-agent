// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_msgs:msg/Encoder.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_MSGS__MSG__DETAIL__ENCODER__BUILDER_HPP_
#define ROBOT_MSGS__MSG__DETAIL__ENCODER__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_msgs/msg/detail/encoder__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_msgs
{

namespace msg
{

namespace builder
{

class Init_Encoder_right_ticks
{
public:
  explicit Init_Encoder_right_ticks(::robot_msgs::msg::Encoder & msg)
  : msg_(msg)
  {}
  ::robot_msgs::msg::Encoder right_ticks(::robot_msgs::msg::Encoder::_right_ticks_type arg)
  {
    msg_.right_ticks = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_msgs::msg::Encoder msg_;
};

class Init_Encoder_left_ticks
{
public:
  explicit Init_Encoder_left_ticks(::robot_msgs::msg::Encoder & msg)
  : msg_(msg)
  {}
  Init_Encoder_right_ticks left_ticks(::robot_msgs::msg::Encoder::_left_ticks_type arg)
  {
    msg_.left_ticks = std::move(arg);
    return Init_Encoder_right_ticks(msg_);
  }

private:
  ::robot_msgs::msg::Encoder msg_;
};

class Init_Encoder_header
{
public:
  Init_Encoder_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Encoder_left_ticks header(::robot_msgs::msg::Encoder::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_Encoder_left_ticks(msg_);
  }

private:
  ::robot_msgs::msg::Encoder msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_msgs::msg::Encoder>()
{
  return robot_msgs::msg::builder::Init_Encoder_header();
}

}  // namespace robot_msgs

#endif  // ROBOT_MSGS__MSG__DETAIL__ENCODER__BUILDER_HPP_
