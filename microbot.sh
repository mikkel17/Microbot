#!/bin/sh
# Launch RuneLite as the alt user
export XAUTHORITY=~/.Xauthority
xhost si:localuser:osrs02
sudo -u osrs01 env/bin/python AutoMining.py
