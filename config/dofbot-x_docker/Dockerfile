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
WORKDIR /home/Dofbot/
# Optional: Add a simple Python script for testing
COPY dofbotx_ros2_setup.bash $WORKDIR
COPY test/ $WORKDIR
RUN source $WORKDIR/dofbotx_ros2_setup.bash
# Entry point or command for debugging (can be overridden)
CMD ["bash"]
