#!/bin/bash

# Usage: ./docker_setup.sh <port_number> <user_name>
# This script starts a Jupyter notebook in a Docker container inside a screen session.
# Arguments:
#   <port_number> - The port on which the Jupyter notebook will be accessible.
#   <user_name> - The username based on which the working directory will be created and named.

# Check for the correct number of arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <port_number> <user_name>"
    exit 1
fi

# Extract arguments
port_number=$1
user_name=$2
working_dir="${user_name}_dir"

# Check if the specified directory exists, create if it doesn't
if [ ! -d "$working_dir" ]; then
    echo "Directory $working_dir does not exist. Creating now..."
    mkdir -p "$working_dir"
    if [ $? -ne 0 ]; then
        echo "Failed to create directory $working_dir. Exiting."
        exit 1
    fi
fi

# Use screen to run Docker in a new session named after the user
screen -dmS $user_name bash -c "docker run -it -p ${port_number}:8888 --user root -e GRANT_SUDO=yes --group-add users \
-v /bigdisk/Trustwatch:/home/jovyan/Trustwatch:ro \
-v ${PWD}/${working_dir}:/home/jovyan/${working_dir} \
jupyter/base-notebook start.sh jupyter notebook --NotebookApp.token=''"

echo "Started Jupyter Notebook in Docker container within screen session named $user_name"
