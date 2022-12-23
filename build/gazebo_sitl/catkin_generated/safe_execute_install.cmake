execute_process(COMMAND "/home/zarquon/Project/SwarmDrone/build/gazebo_sitl/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/zarquon/Project/SwarmDrone/build/gazebo_sitl/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
