#!/bin/sh
# Launch RuneLite as the alt user

cd /opt/microbot
export XAUTHORITY=~/.Xauthority
xhost si:localuser:$1
sudo -u $1 java -jar microbot.jar
