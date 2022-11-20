#!/bin/sh

SESSIONNAME="delivery_bot"
tmux has-session -t $SESSIONNAME

if [ $? != 0 ]
 then
 tmux new-session -s $SESSIONNAME -d
 tmux send-keys -t $SESSIONNAME "sleep 15" C-m
 tmux send-keys -t $SESSIONNAME "cd ~/Delivery-bot" C-m
 tmux send-keys -t $SESSIONNAME "/root/.local/share/pypoetry/venv/bin/poetry run python -m src.main" C-m
fi