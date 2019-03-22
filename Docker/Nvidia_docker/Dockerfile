FROM osrf/ros:melodic-desktop-full-bionic

ENV NVIDIA_VISIBLE_DEVICES \
    ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES \
    ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics

RUN mkdir -p ~/catkin_ws/src
RUN cd ~/catkin_ws/src && git clone https://github.com/robo-jordo/quadruped_ml_gait.git rupert_learns
RUN cd ~/catkin_ws/src && git clone https://github.com/ros-simulation/gazebo_ros_demos.git
RUN apt-get install ros-melodic-gazebo-ros-pkgs ros-melodic-gazebo-ros-control
RUN apt-get update
RUN apt-get install nano
RUN apt-get -y install ros-melodic-ros-control ros-melodic-ros-controllers
RUN /bin/bash -c '. /opt/ros/melodic/setup.bash; cd ~/catkin_ws; catkin_make'
RUN /bin/bash -c '. /opt/ros/melodic/setup.bash; cd ~/catkin_ws; source devel/setup.bash'
CMD ["bash"]
