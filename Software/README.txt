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
	add i2c-dev
	# /etc/modules: kernel modules to load at boot time.
	#
	# This file contains the names of kernel modules that should be loaded
	# at boot time, one per line. Lines beginning with "#" are ignored.
	# Parameters can be specified after the module name.

	snd-bcm2835
	i2c-dev
	
now reboot
	sudo reboot

