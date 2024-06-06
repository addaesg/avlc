# I AM A SINGLE LADY O A A A A
cmake_minimum_required(VERSION 3.29)
project(ciculu)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O2")

set(SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/src)
set(BIN_DIR ${CMAKE_CURRENT_SOURCE_DIR}/bin)

file(GLOB_RECURSE SOURCE_FILES ${SOURCE_DIR}/*.cpp ${SOURCE_DIR}/*.c)

add_executable(ciculu ${SOURCE_FILES})
set_target_properties(ciculu PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${BIN_DIR}
)

