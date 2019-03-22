# Rupert learns to walk

This project aims to use machine learning to train a quadrupedal robot to walk. The machine learning is done in simulation using ROS and gazebo. Once the gait is learned it is implemented on a physical 3D printed quadruped that is actuated using hobby servo motors.

This project focused on an implemnetation of evolutionary algorithms in order to have a robot learn a gait. However the underlying framework that has been set up to acheive this can be used for many other applications in machine learning that uses simulation.

## Motivation 
This project was developed by me as a winter project credit while completing a Master's in Robotics at Northwestern University.
The project aims to blend an interest in machine learning with real world robots. This is acheived through setting up a simulation environment that allows for training of machine learning models for robots in simulation.

## Screenshots

## Getting started
### Pre requisites and variations
In order to run this project without having to install ROS and the the dependancies and packages required a docker container has been developed.

#### Docker
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

Note: If you have named the conatiner something other than rupert_full when building you will have to change the `rupert.bash` file to reflect this change.

Opening a second terminal in the already running conatiner

`$ sudo docker exec -it <container_name> /bin/bash`

### Built with

### Running the Docker conatiner

## Using the framework

## Results

## Credit