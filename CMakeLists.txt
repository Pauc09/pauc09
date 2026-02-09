cmake_minimum_required(VERSION 3.10)
project(OpenCV)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(OpenCV REQUIRED)

add_executable(show_image src/show_image.cpp)
target_link_libraries(show_image ${OpenCV_LIBS})

add_executable(show_camera src/show_camera.cpp)
target_link_libraries(show_camera ${OpenCV_LIBS})
