Expand your partition, set password, set you timezone and keyboard, overclock to 800Mhz, i suggest to no start desktop mode (you need only the console mode) for fast boot then select finish for save and reboot.

start with an update.
	sudo apt-get update  

#install REDIS (redis is a database)
	sudo apt-get install redis-server

#to use REDIS on Python#
	sudo apt-get install python-setuptools
	sudo easy_install redis
	
#to use REDIS on PHP#
1) Preparation
	sudo apt-get install php5-dev
note (php5-dev provides the dev library as well as the phpize command which is required for the compiling step)
2) Get phpredis source code, should be pretty easy by running
	git clone git://github.com/nicolasff/phpredis.git
3) Compile and install
		cd phpredis
		phpize
		./configure
		make
		sudo -s make install
4) Enable the phpredis extension
		sudo -s
		echo "extension=redis.so">/etc/php5/conf.d/redis.ini
		exit
		cd .. (go to home)
		
#GIT (optiona)#
	git clone https://github.com/davidecaminati/Domotica-Raspberry.git
	
#SPI#
Enabling the SPI kernel module
As root, edit the kernel module blacklist file:
	sudo nano /etc/modprobe.d/raspi-blacklist.conf

Comment out the spi-bcm2708 line so it looks like this:
	#blacklist spi-bcm2708

Save the file so that the module will load on future reboots. To enable the module now, enter:
		sudo modprobe spi-bcm2708

Now, if you run the lsmod command, you should see something like:
	lsmod
	Module                  Size  Used by
	spi_bcm2708             4421  0
	
#SPIDEV#
	sudo apt-get install python-pip  
	sudo pip install spidev
	sudo pip install python-dev
	sudo apt-get install python-imaging python-imaging-tk python-pip python-dev git
	mkdir python-spi
	cd python-spi
	wget https://raw.github.com/doceme/py-spidev/master/setup.py
	wget https://raw.github.com/doceme/py-spidev/master/spidev_module.c
	sudo python setup.py install
	cd ..
	sudo pip install wiringpi
	
#MODULE I2C#
	sudo apt-get install python-smbus
	sudo apt-get install i2c-tools (usefull but not essential)
	sudo modprobe i2c-dev
	sudo modprobe i2c-bcm2708

	sudo nano /etc/modules
	#add this line#
		i2c-dev
	# /etc/modules: kernel modules to load at boot time.
	#
	# This file contains the names of kernel modules that should be loaded
	# at boot time, one per line. Lines beginning with "#" are ignored.
	# Parameters can be specified after the module name.

	snd-bcm2835
	i2c-dev

#enable 1wire#
	sudo modprobe w1-gpio
	sudo modprobe w1-therm
	
#enable TFT display# 
	#guide http://www.raspberrypi.org/phpBB3/viewtopic.php?f=64&t=48967#
	#model http://www.raspberrypi.org/phpBB3/viewtopic.php?f=59&t=48956#
	
	sudo wget https://raw.github.com/Hexxeh/rpi-update/master/rpi-update -O /usr/bin/rpi-update && sudo chmod +x /usr/bin/rpi-update
	
	sudo mv /lib/modules/$(uname -r) /lib/modules/$(uname -r).bak
	sudo REPO_URI=https://github.com/notro/rpi-firmware rpi-update
	sudo shutdown -r now
	
	sudo modprobe fbtft dma
	sudo modprobe fbtft_device name=hy28a rotate=270 speed=48000000 fps=50
	#Then to configure the touch panel#
		sudo modprobe ads7846_device pressure_max=255 y_min=190 y_max=3850 gpio_pendown=17 x_max=3850 x_min=230 x_plate_ohms=100 swap_xy=1 verbose=3

		sudo nano /etc/modules
		#and add#
			fbtft dma
			fbtft_device name=hy28a rotate=270 speed=48000000 fps=50
			ads7846_device pressure_max=255 y_min=190 y_max=3850 gpio_pendown=17 x_max=3850 x_min=230 x_plate_ohms=100 swap_xy=1 verbose=3
		#now reboot#
			sudo reboot
		
	#In order to use the touch panel with python, X, and to calibrate it, a few packages need loading :#

		sudo apt-get update	
		sudo apt-get install libts-bin evtest xinput
		sudo pip install evdev

	#To calibrate the touch panel#
		sudo TSLIB_FBDEVICE=/dev/fb1 TSLIB_TSDEVICE=/dev/input/event0 ts_calibrate
		
#enable midori on TFT#
	sudo nano /boot/cmdline.txt
	#at the end of line add this#
		fbcon=map:10 fbcon=font:VGA8x8
	#set autostart#
		sudo nano /etc/xdg/lxsession/LXDE/autostart
		#write at the end of the file#		
			@xset s off
			@xset -dpms
			@xset s noblank
			@midori -e Fullscreen -a http://IP-OF-YOUR_SERVER/mobile
	#Auto startx: modify this file #
		sudo nano /etc/rc.local
		#after fi and before exit 0#
		#add this line#
			su -l pi -c "env FRAMEBUFFER=/dev/fb1 startx &"
		#fix error calibration#
			sudo nano /usr/share/X11/xorg.conf.d/10-evdev.conf
		#find Input Class of touchscreen and before that EndSection insert a new line:
			Option "InvertY" "true"
		#remove the mouse pointer#
			sudo apt-get install unclutter
		#reboot#
			sudo reboot
	
#toggle light on the TFT#
	sudo nano /sys/class/backlight/fb_ili9320/bl_power
	#toggle 1 = (on) or 0 = (off)#


#if you want to test now the capability of your  powerful Raspberry go to 

