project(detect_markers)

cmake_minimum_required(VERSION 2.8)

set(CMAKE_CXX_STANDARD 11)

find_package(OpenCV REQUIRED)

add_executable(detect_markers_images src/detect_markers_images.cpp)

target_link_libraries(detect_markers_images ${OpenCV_LIBS})
