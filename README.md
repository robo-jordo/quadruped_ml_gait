# Rupert learns to walk

This project aims to use machine learning to train a quadrupedal robot to walk. The machine learning is done in simulation using ROS and gazebo. Once the gait is learned it is implemented on a physical 3D printed quadruped that is actuated using hobby servo motors. The model I used can be found on thingiverse. ............

This project focused on an implemnetation of evolutionary algorithms in order to have a robot learn a gait. However the underlying framework that has been set up to acheive this can be used for many other applications in machine learning that uses simulation.

## Motivation 
This project was developed by me as a winter project credit while completing a Master's in Robotics at Northwestern University.
The project aims to blend an interest in machine learning with real world robots. This is acheived through setting up a simulation environment that allows for training of machine learning models for robots in simulation.

## Screenshots
<img src="/img/rupert.png" width="300" title="3D printed robot"/> <img src="/img/rupert_sim.png" width="325" title="Simulated robot"/> 

3D printed robot and simulated model.

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

`$ sudo docker build -t <CONTAINER_NAME> .`

In order to run the docker file with the correct parameters each directory has a bash script that can be run.

Running the conatiner:

`$ sudo ./rupert.bash <CONTAINER_NAME>`

At this point you can move forward to the 'Using the framework part'.

Note: If you have named the conatiner something other than rupert_full when building you will have to change the `rupert.bash` file to reflect this change.


Opening a second terminal in the already running conatiner

`$ sudo docker exec -it <CONTAINER_ID> /bin/bash`

If you are not familiar with Docker the countainer ID can be found with:

`$ sudo docker ps -a`

#### 2) Standard (without Docker)
------
##### Requirements
This method requires:

* [Linux Ubuntu 18.04](https://www.ubuntu.com/download/desktop)
* [Ros Melodic](http://wiki.ros.org/melodic)-Full installation
Package dependancies:
[gazebo_ros_demos](https://github.com/ros-simulation/gazebo_ros_demos.git)

Install ros dependancies:

* `$ sudo apt-get install ros-melodic-gazebo-ros-pkgs ros-melodic-gazebo-ros-control`

* `$ apt-get install ros-melodic-ros-control ros-melodic-ros-controllers`

You may then clone this repository into a catkin workspace and move forward to using the framework.

### Built with

* [Linux Ubuntu 18.04](https://www.ubuntu.com/download/desktop)
* [Ros Melodic](http://wiki.ros.org/melodic)
* [Docker](https://docs.docker.com/get-started/)

## Using the framework
In order to use the framework there are multiple steps.
The framework has been designed to allow a user to first launch the simulation, then either:

* Use the genetic algorithm which is in this repository which has changeable parameters.
* Write your own algorithm to use with the gazebo simulation using ros topics and services.

### Launching the simulation
To launch the simulation once you are in the Docker container's shell run the following commands.
```
$ cd
$ source /opt/ros/melodic/setup.bash
$ cd catkin_ws
$ source devel/setup.bash
$ roslaunch rupert_learns rupert.launch
```

To launch the simulation in your own system you will need to run the following commands.
```
$ source /opt/ros/melodic/setup.bash
```

**Make sure you are in your catkin workspace**

```
$ catkin_make
$ source devel/setup.bash
$ roslaunch rupert_learns rupert.launch
```

This will launch rviz and gazebo you should see a model of the robot in both, it will likely be in a strange pose.

### Running the evolutionary algorithm
If you are using docker you will now need to open a new shell in the existing container as described above, this can be done with the command.

`$ sudo docker exec -it <CONTAINER_ID> /bin/bash`

The evolutionary algorithm requires one line to run. 

`$ rosrun rupert_learns rupert_genetic_algorithm.py`

You should now be able to see the robot wiggle around a bit in gazebo and then dissapear and be replaced by a new robot at the origin. In the terminal you will see the individual numbers as they go and the fitness score that they earned.

The script allows for changing certain parameters.
The changeable parameters are set as global variables at the top of the [rupert_genetic_algorithm](/src/rupert_genetic_algorithm.py) script. 

These variables are:

* population_size (integer): This will determine the number of individuals in each generation.
* length (integer): This determines the length of the genetic encoding string (i.e. list of joint positions that are evolved).
* static_hip (boolean): If True the hips will never move, if false the hip joints will be a part of the genetic encoding and will move.
* hip_position (float): This is the poition you would like the hips to be in if you choose static_hip to be true.
* phased_gait (boolean): If True this changes the genetic encoding from being one long list of joint angles which is spilt to determine which joint moves where to a list of joint positions and 3 offset values. This effectively evolves one set of joint transitions and applies it to all the legs with a phase offset determined by the evolved phase list.
* bias (boolean): If true this makes the joints more likely to form angles that point the legs downwards.
* probabilistic_cull (boolean): If True this will kill members in the population based on their fitness but it will be probabilistic i.e the stranger the individual the more likely they are to survive but there is no guarantee. If False the fittest 50% of the population are guaranteed to survive.
* generations (integer): This determines the number of generations that the algorithm will go through.
* switch_mutation_gen (integer): This will determine the generation at which to lower the mutation rates.


## Results


## Credit