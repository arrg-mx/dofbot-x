# Base image
FROM dustynv/ros:humble-desktop-l4t-r32.7.1
# Update and install required packages
ARG PYTHON_VERSION_ARG="3.10"
RUN apt-get update && apt-get install -y --no-install-recommends \
    i2c-tools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHON_VERSION=${PYTHON_VERSION_ARG} \
PIP_DISABLE_PIP_VERSION_CHECK=on \
PIP_DEFAULT_TIMEOUT=100 \
PYTHONFAULTHANDLER=1 \
PYTHONUNBUFFERED=1 \
PYTHONIOENCODING=utf-8 \
PYTHONHASHSEED=random \
PIP_NO_CACHE_DIR=off \
PIP_CACHE_PURGE=true \
PIP_ROOT_USER_ACTION=ignore \
TWINE_NON_INTERACTIVE=1 \
DEBIAN_FRONTEND=noninteractive

COPY py_install.sh /tmp/install_python.sh 
RUN /tmp/install_python.sh

# Set the working directory inside the container
# The WORKDIR instruction sets the working directory for any RUN, CMD, ENTRYPOINT, COPY and ADD instructions that follow it in the Dockerfile. 
# If the WORKDIR doesn’t exist, it will be created even if it’s not used in any subsequent Dockerfile instruction.
WORKDIR /home/Dofbot/
# Optional: Add a simple Python script for testing
COPY dofbotx_ros2_setup.bash /home/Dofbot/
COPY tools/ /home/Dofbot/
# RUN source /home/Dofbot/dofbotx_ros2_setup.bash
# Entry point or command for debugging (can be overridden)
CMD ["bash"]
ENV ROS_DOMAIN_ID=10
ENV ROS2_DOFBOTX_WS='/home/Dofbot/ws_dofbot-x'
