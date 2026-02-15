cmake_minimum_required(VERSION 3.10)
project(Punto2_Saturacion)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

add_executable(punto2 main.cpp)
target_link_libraries(punto2 ${OpenCV_LIBS})

message(STATUS "OpenCV version: ${OpenCV_VERSION}")
message(STATUS "OpenCV libraries: ${OpenCV_LIBS}")
message(STATUS "OpenCV include directories: ${OpenCV_INCLUDE_DIRS}")
