# Install script for directory: /home/skysar/Documents/spring18/EE5531/lab3/royalpotato/jackal_navigation/src/pointgrey_camera_driver/pointgrey_camera_description

# Set the install prefix
IF(NOT DEFINED CMAKE_INSTALL_PREFIX)
  SET(CMAKE_INSTALL_PREFIX "/home/skysar/Documents/spring18/EE5531/lab3/royalpotato/jackal_navigation/install")
ENDIF(NOT DEFINED CMAKE_INSTALL_PREFIX)
STRING(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
IF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  IF(BUILD_TYPE)
    STRING(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  ELSE(BUILD_TYPE)
    SET(CMAKE_INSTALL_CONFIG_NAME "")
  ENDIF(BUILD_TYPE)
  MESSAGE(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
ENDIF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)

# Set the component getting installed.
IF(NOT CMAKE_INSTALL_COMPONENT)
  IF(COMPONENT)
    MESSAGE(STATUS "Install component: \"${COMPONENT}\"")
    SET(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  ELSE(COMPONENT)
    SET(CMAKE_INSTALL_COMPONENT)
  ENDIF(COMPONENT)
ENDIF(NOT CMAKE_INSTALL_COMPONENT)

# Install shared libraries without execute permission?
IF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  SET(CMAKE_INSTALL_SO_NO_EXE "1")
ENDIF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/skysar/Documents/spring18/EE5531/lab3/royalpotato/jackal_navigation/build/pointgrey_camera_driver/pointgrey_camera_description/catkin_generated/installspace/pointgrey_camera_description.pc")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/pointgrey_camera_description/cmake" TYPE FILE FILES
    "/home/skysar/Documents/spring18/EE5531/lab3/royalpotato/jackal_navigation/build/pointgrey_camera_driver/pointgrey_camera_description/catkin_generated/installspace/pointgrey_camera_descriptionConfig.cmake"
    "/home/skysar/Documents/spring18/EE5531/lab3/royalpotato/jackal_navigation/build/pointgrey_camera_driver/pointgrey_camera_description/catkin_generated/installspace/pointgrey_camera_descriptionConfig-version.cmake"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/pointgrey_camera_description" TYPE FILE FILES "/home/skysar/Documents/spring18/EE5531/lab3/royalpotato/jackal_navigation/src/pointgrey_camera_driver/pointgrey_camera_description/package.xml")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/pointgrey_camera_description" TYPE DIRECTORY FILES
    "/home/skysar/Documents/spring18/EE5531/lab3/royalpotato/jackal_navigation/src/pointgrey_camera_driver/pointgrey_camera_description/launch"
    "/home/skysar/Documents/spring18/EE5531/lab3/royalpotato/jackal_navigation/src/pointgrey_camera_driver/pointgrey_camera_description/meshes"
    "/home/skysar/Documents/spring18/EE5531/lab3/royalpotato/jackal_navigation/src/pointgrey_camera_driver/pointgrey_camera_description/rviz"
    "/home/skysar/Documents/spring18/EE5531/lab3/royalpotato/jackal_navigation/src/pointgrey_camera_driver/pointgrey_camera_description/urdf"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

