Please note:
This code is not mantained anymore, some part are vulnerable, please don't use
in productrion, use only for reference.

Domotics
========

The goal is to create an AI (Artificial Intelligence) with a personality to 
interact with using Natural Interfaces (such as speek, gesture...) and improve 
the home's comfort without spending too much money.

This system is composed by at least 5 Raspberry Pi (rev 2) ...
each of them will be used for a different functionality (ex. thermal probe, display TFT...)


Full system is composed by:

* 5 (or more) Raspberry PI
* 1 TFT display 2,8" touch
* 1 Kinect (for XBOX 360)
* 2 Webcam Logitech HD (C525)
* 1 Powered HUB (Trust 7 port)
* 1 Temperature sensor digital (DS18S20)
* 1 Temperature sensor analogic (LM35DZ)
* 3 Port expander i2c  (MCP23017)
* 1 DAC digital analogic converter (MCP3008)
* 2 Magnetic contact 
* 1 Relays board with 8 relays and 8 input 
* 3 RGB led  (3w power)
* 3 Bulb RGB led 9 W with remote (hacked)


HOW TO START
------------

Download the sdcard image named 2013-05-25-wheezy-raspbian-2013-07-07-fbtft.img 
from http://tronnes.org/fbtft/download.html (this image support Framebuffer module for TFT display) 
or new image file from this url
http://downloads.raspberrypi.org/raspbian_latest


and 
flash the SD Card, (find guide on http://elinux.org/RPi_Easy_SD_Card_Setup i suggest to use Win32DiskImager)

For the first step of configuration look
[here](Software/README.md)

