# Setting ROS2 DOMAIN to ARRG channel (default value)
export ROS_DOMAIN_ID=10
# Source DofbotX ROS2 Wrokspace
source /home/Dofbot/ws_dofbot-x/install/setup.bash
# Alias declarations
alias srcthis='source /home/Dofbot/ws_dofbot-x/install/setup.bash'
alias ros2path='sed "s/:/\n/g" <<< "$AMENT_PREFIX_PATH" | sort | uniq'
alias rospath='tr ":" "\n" <<< "$AMENT_PREFIX_PATH" | sort | uniq'