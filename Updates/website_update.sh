#!/bin/bash
clear
echo "Starting Script now....."
echo "This script will delete all your file in www and download the updated fil$
cd /home/pi/Domotics-Raspberry/
git pull
sudo rm -r /var/www/*
sudo cp -r /home/pi/Domotics-Raspberry/Web_site/www/* /var/www/
killall midori
su -l pi -c "env FRAMEBUFFER=/dev/fb1 startx &"