source /opt/ros/noetic/setup.bash
catkin_make
killall -9 gzserver
killall -9 gzclient
source activate
conda activate Noetic
cd ~/PX4-Autopilot/
DONT_RUN=1 make px4_sitl_default gazebo
source ~/Project/Mav/devel/setup.bash
source ~/Project/SwarmDrone/devel/setup.bash 
source Tools/simulation/gazebo/setup_gazebo.bash $(pwd) $(pwd)/build/px4_sitl_default 
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd)
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd)/Tools/simulation/gazebo/sitl_gazebo
roslaunch gazebo_sitl start_3-multi_sitl.launch