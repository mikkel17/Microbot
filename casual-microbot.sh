#!/bin/sh
# Launch RuneLite as the alt user
cd /opt/microbot
export XAUTHORITY=~/.Xauthority
xhost si:localuser:osrs01
sudo -u osrs01 java -jar microbot.jar
