add_library(glad 
    ${CMAKE_CURRENT_SOURCE_DIR}/src/glad.c
)

target_include_directories(glad
    PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include/
)

if (SYSTEM_NAME MATCHES "Linux")
    target_compile_options(glad PRIVATE -fPIC)
endif()