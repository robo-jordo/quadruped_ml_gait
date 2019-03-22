FROM osrf/ros:melodic-desktop-full-bionic

RUN mkdir -p ~/catkin_ws/src
RUN cd ~/catkin_ws/src && git clone https://github.com/robo-jordo/quadruped_ml_gait.git
RUN cd ~/catkin_ws/src && git clone https://github.com/ros-simulation/gazebo_ros_demos.git
RUN apt-get install ros-melodic-gazebo-ros-pkgs ros-melodic-gazebo-ros-control
RUN /bin/bash -c '. /opt/ros/melodic/setup.bash; cd ~/catkin_ws; catkin_make'
RUN /bin/bash -c '. /opt/ros/melodic/setup.bash; cd ~/catkin_ws; source devel/setup.bash'
CMD ["bash"]