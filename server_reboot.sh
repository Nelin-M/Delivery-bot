#!/bin/sh

tmux kill-session -t delivery_bot
sleep 10
docker-compose down
sleep 15
reboot
