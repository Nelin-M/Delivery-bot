#!/bin/sh

tmux kill-session -t delivery_bot
sleep 10
docker compose stop
sleep 15
reboot
