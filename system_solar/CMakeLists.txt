## -------------------------------------------------------------------------
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## -------------------------------------------------------------------------

cmake_minimum_required(VERSION 3.10)

project(SolarSystem)

find_package(Boost REQUIRED)
find_package(OpenGL COMPONENTS OpenGL REQUIRED)
find_package(GLUT REQUIRED)

add_executable(solar_system Controller.cxx SolarSystem.cxx main.cxx)
target_link_libraries(
  solar_system
  ${Boost_LIBRARIES}
  OpenGL::OpenGL
  GLUT::GLUT
  )

## eof - CMakeLists.txt
