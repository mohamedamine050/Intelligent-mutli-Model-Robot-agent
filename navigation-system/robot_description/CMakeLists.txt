cmake_minimum_required(VERSION 3.8)
project(robot_description)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)

# Install URDF files
install(
  DIRECTORY urdf
  DESTINATION share/${PROJECT_NAME}
)

# Install launch files
install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

# Install RViz config files
install(
  DIRECTORY rviz
  DESTINATION share/${PROJECT_NAME}
)

# Install meshes (if you have any 3D models)
# install(
#   DIRECTORY meshes
#   DESTINATION share/${PROJECT_NAME}
# )

ament_package()