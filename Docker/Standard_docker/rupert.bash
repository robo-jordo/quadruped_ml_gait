#!/usr/bin/env bash

if (( $# == 1 )); then
    sudo docker run -it \
        --env="DISPLAY" \
        --env="QT_X11_NO_MITSHM=1" \
        --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
        $1 
else
        echo "No container name given"
fi

export containerId=$(sudo docker ps -l -q)
xhost +local:`sudo docker inspect --format='' $containerId`
sudo docker start $containerId