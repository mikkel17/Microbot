#!/bin/sh
# Launch RuneLite as the alt user

cd /opt/Microbot
export XAUTHORITY=~/.Xauthority
xhost si:localuser:$1
sudo -u $1 env/bin/python start_jvm.py $1
