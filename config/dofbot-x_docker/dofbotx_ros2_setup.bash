# Alias declarations
alias srcthis='source /home/Dofbot/ws_dofbot-x/install/setup.bash'
alias ros2path='sed "s/:/\n/g" <<< "$AMENT_PREFIX_PATH" | sort | uniq'
alias rospath='tr ":" "\n" <<< "$AMENT_PREFIX_PATH" | sort | uniq'
