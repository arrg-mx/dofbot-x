# Base image
FROM dustynv/ros:humble-desktop-l4t-r32.7.1
# Update and install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    i2c-tools \
    python3-smbus \
    python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
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
