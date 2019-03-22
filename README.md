# Rupert learns to walk

This project aims to use machine learning to train a quadrupedal robot to walk. The machine learning is done in simulation using ROS and gazebo. Once the gait is learned it is implemented on a physical 3D printed quadruped that is actuated using hobby servo motors. The model I used can be found on thingiverse. ............

This project focused on an implemnetation of evolutionary algorithms in order to have a robot learn a gait. However the underlying framework that has been set up to acheive this can be used for many other applications in machine learning that uses simulation.

## Motivation 
This project was developed by me as a winter project credit while completing a Master's in Robotics at Northwestern University.
The project aims to blend an interest in machine learning with real world robots. This is acheived through setting up a simulation environment that allows for training of machine learning models for robots in simulation.

## Screenshots
<figure><img src="/img/rupert.png" width="300" title="3D printed robot"/><figcaption>3D printed robot</figcaption><img src="/img/rupert_sim.png" width="325" title="Simulated robot"/></figure>
## Contents of the repository

## Getting started
### Pre requisites and variations
There are two ways to run this project.
1) Docker 
2) Standard set up

In order to run this project without having to install ROS and the the dependancies and packages required a docker container has been developed. this is the reccomended way to run this project.

#### 1) Docker
------
##### Requirements
To use this project with the Docker conatiner you will need Docker installed on [Linux](https://docs.docker.com/get-started/).

There are two different Docker containers that can be found in this repo :
* Standard linux machine
* Linux machine with Nvidia drivers

##### Running the Docker conatiners

In order to build and run the Docker conatiners you will need to download the contents of the [Docker](/Docker) directory.
This directory then contains two sub directories:
* [Standard_docker](/Docker/Standard_docker): Linux computers without GPU/Nvidia drivers
* [Nvidia_docker](/Docker/Nvidia_docker): Linux computers with a Nvidia GPU driver

You will need to pick the appropriate container for your system.

Building the container:

**Ensure you are in either the Standard_docker directory or the Nvidia_docker directory.**

`$ sudo Docker build -t rupert_full .`

In order to run the docker file with the correct parameters each directory has a bash script that can be run.

Running the conatiner:

`$ sudo ./docker rupert.bash`

At this point you can move forward to the 'Using the framework part'.

Note: If you have named the conatiner something other than rupert_full when building you will have to change the `rupert.bash` file to reflect this change.


Opening a second terminal in the already running conatiner

`$ sudo docker exec -it <container_name> /bin/bash`

#### 2) Standard (without Docker)
------
##### Requirements
This method requires:
*[Linux Ubuntu 18.04](https://www.ubuntu.com/download/desktop)
*[Ros Melodic](http://wiki.ros.org/melodic)-Full installation
Package dependancies:
[gazebo_ros_demos](https://github.com/ros-simulation/gazebo_ros_demos.git)

Install ros dependancies:

*`$ sudo apt-get install ros-melodic-gazebo-ros-pkgs ros-melodic-gazebo-ros-control`

*`$ apt-get install ros-melodic-ros-control ros-melodic-ros-controllers`

You may then clone this repository into a catkin workspace and move forward to using the framework.

### Built with
*[Linux Ubuntu 18.04](https://www.ubuntu.com/download/desktop)
*[Ros Melodic](http://wiki.ros.org/melodic)
*[Docker](https://docs.docker.com/get-started/)

## Using the framework

## Results

## Credit