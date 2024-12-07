# Base image
FROM dustynv/ros:humble-desktop-l4t-r32.7.1
ARG MYHOME=/root
ENV MYHOME ${MYHOME}
ARG PYTHONVER=3.10.14
ENV PYTHONVER ${PYTHONVER}
ARG PYTHONNAME=base
ENV PYTHONNAME ${PYTHONNAME}
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y locales wget git curl zip vim apt-transport-https tzdata language-pack-nb language-pack-nb-base manpages \
    build-essential libjpeg-dev libssl-dev xvfb zlib1g-dev libbz2-dev libreadline-dev libreadline6-dev libsqlite3-dev tk-dev libffi-dev libpng-dev libfreetype6-dev \
    libx11-dev libxtst-dev libfontconfig1 lzma lzma-dev

RUN git clone https://github.com/pyenv/pyenv.git ${MYHOME}/.pyenv && \
    git clone https://github.com/yyuu/pyenv-virtualenv.git ${MYHOME}/.pyenv/plugins/pyenv-virtualenv && \
    git clone https://github.com/pyenv/pyenv-update.git ${MYHOME}/.pyenv/plugins/pyenv-update

SHELL ["/bin/bash", "-c", "-l"]

COPY ./.bash_profile  /tmp/
RUN cat /tmp/.bash_profile >> ${MYHOME}/.bashrc && \
    cat /tmp/.bash_profile >> ${MYHOME}/.bash_profile && \
    rm -f /tmp/.bash_profile && \
    source ${MYHOME}/.bash_profile && \
    pyenv install ${PYTHONVER} && \
    pyenv virtualenv ${PYTHONVER} ${PYTHONNAME} && \
    pyenv global ${PYTHONNAME}

COPY requirements.txt /tmp/requirements.txt

# Install pip for Python 3.10 and smbus2 package
RUN python -m ensurepip --upgrade && \
    python -m pip install --upgrade pip && \
    python -m pip install -r /tmp/requirements.txt

# Add a verification script to confirm Python version and smbus installation
COPY verify_python.py /tmp/verify_python.py
RUN python /tmp/verify_python.py

# Add runtime validation scripts
COPY validate_smbus.py /usr/local/bin/validate_smbus.py
COPY validate_smbus2.py /usr/local/bin/validate_smbus2.py
RUN chmod +x /usr/local/bin/validate_smbus.py /usr/local/bin/validate_smbus2.py

# Set the working directory
WORKDIR /home/Dofbot/

# Copy necessary files
COPY dofbotx_ros2_setup.bash /home/Dofbot/
# COPY tools/ /home/Dofbot/

# Default command for debugging (can be overridden)
CMD ["bash"]

# Environment variables
ENV ROS_DOMAIN_ID=10
ENV ROS2_DOFBOTX_WS='/home/Dofbot/ws_dofbot-x'

