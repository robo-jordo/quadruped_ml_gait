#!/usr/bin/env bash
sudo docker run -it \
    --env="DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    ros_test2 \

export containerId=$(sudo docker ps -l -q)
xhost +local:`sudo docker inspect --format='' $containerId`
sudo docker start $containerId