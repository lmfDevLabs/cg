## -------------------------------------------------------------------------
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## -------------------------------------------------------------------------

include_directories(
  ${PROJECT_BINARY_DIR}/lib
  ${PROJECT_SOURCE_DIR}/lib
  )

add_executable(RoboticArm RoboticArm.cxx)
target_link_libraries(RoboticArm PUJ_CGraf)

## eof - CMakeLists.txt
