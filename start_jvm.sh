#!/bin/sh
# Launch RuneLite as the alt user
cd /opt/Microbot
export XAUTHORITY=~/.Xauthority
xhost si:localuser:osrs01
sudo -u osrs01 env/bin/python start_jvm.py
