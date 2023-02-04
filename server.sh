#!/bin/sh

SESSION_NAME="delivery_bot"
tmux has-session -t $SESSION_NAME

if [ $? != 0 ]
 then
 tmux new-session -s $SESSION_NAME -d
 tmux send-keys -t $SESSION_NAME "docker compose start" C-m
 tmux send-keys -t $SESSION_NAME "sleep 15" C-m
 tmux send-keys -t $SESSION_NAME "cd ~/Delivery-bot" C-m
 tmux send-keys -t $SESSION_NAME "/root/.local/share/pypoetry/venv/bin/poetry run python -m src.main" C-m
fi