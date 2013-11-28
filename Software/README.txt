Expand your partition, set password, set you timezone and keyboard, overclock to 800Mhz, i suggest to no start desktop mode (you need only the console mode) for fast boot then select finish for save and reboot.
#copy the repository#
	git clone https://github.com/davidecaminati/Domotics-Raspberry

#start with an update#
	sudo apt-get update  

#install REDIS (redis is a database)
	sudo apt-get install redis-server

#to use REDIS on Python#
	sudo apt-get install python-setuptools
	sudo easy_install redis
	#configure binding#
		sudo nano /etc/redis/redis.conf
		#remark bind 127.0.0.1 putting a # infront of the line#
		#bind 127.0.0.1
	
	
#to use REDIS on PHP#
	#Preparation#
		sudo apt-get install php5-dev
	#note (php5-dev provides the dev library as well as the phpize command which is required for the compiling step)#
	#Get phpredis source code, should be pretty easy by running#
		git clone git://github.com/nicolasff/phpredis.git
	#Compile and install#
			cd phpredis
			phpize
			./configure
			make
			sudo -s make install
	#Enable the phpredis extension#
			sudo -s
			echo "extension=redis.so">/etc/php5/conf.d/redis.ini
			exit
			cd .. (go to home)
		
#SPI#
	#Enabling the SPI kernel module#
	#As root, edit the kernel module blacklist file:#
		sudo nano /etc/modprobe.d/raspi-blacklist.conf

	#Comment out the spi-bcm2708 line so it looks like this:#
		#blacklist spi-bcm2708

	#Save the file so that the module will load on future reboots. To enable the module now, enter:#
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
	sudo nano /etc/modules
	#add this lines#
	w1-gpio
	w1-therm
	
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
		#write at the end of the file suggest to use 127.0.0.1 as IP-OF-YOUR_SERVER#		
			@xset s off
			@xset -dpms
			@xset s noblank
			@midori -e Fullscreen -a http://127.0.0.1/mobile
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

#configure web server#
	sudo apt-get install apache2 php5 libapache2-mod-php5
	sudo rm /var/www/index.html
	sudo cp -r /home/pi/Domotics-Raspberry/Web_site/www/* /var/www/
	#set the redis server#
	

#configure analog probe#
	crontab -e
	#add at the end of the file#
	* * * * * sudo python /home/pi/Domotics-Raspberry/Hardware/Analog\ Temperature\ Probe/mcp3008_lm35.py

#configuration to read external temp from internet#
#suggest to add this script in Display raspberry#
	crontab -e
	#add at the end of the file#
	* * * * * sh /home/pi/Domotics-Raspberry/Hardware/Display\ TFT/02_update_external_temp.sh
	
#configure digital probe (my_room_1)#
	#make executable the script#
	chmod +x /home/pi/Domotics-Raspberry/Hardware/Digital\ Temperature\ Probe/02_read_temp_from_probe.sh
	chmod +x /home/pi/Domotics-Raspberry/Hardware/Digital\ Temperature\ Probe/05_send_temp_to_redis.sh
	
	#add the script to crontab#
	crontab -e
	#add at the end of the file#
	* * * * * /home/pi/Domotics-Raspberry/Hardware/Digital\ Temperature\ Probe/05_send_temp_to_redis.sh
	#NOTE#
	#be sure to have activate 1 wire module otherwise look #enable 1wire# #

#configure analogic probe(my_room_2)#
	#switch to root#
	su
	#type password to being root#
	
	#add the script to crontab#
		crontab -e
		#add at the end of the file#
		* * * * * python /home/pi/Domotics-Raspberry/Hardware/Analog\ Temperature\ Probe/mcp3008_lm35.py

#Update a device#
	#in Update directory, you will find usefull script to automate this#
	cd /home/pi/Domotics-Raspberry/Update
	
#error in editing file from windows#
	#if you need to create a  new bash script from windows , pay attention to new line characters , in Win are different than unix#
	#so if you want to sure your file are compatible , you coud install an utility to convert file in unix style#
		sudo apt-get install dos2unix
		#how to use this utility#
		dos2unix <file to convert>
		
#configure wireless#
# for help http://www.linux.com/learn/tutorials/374514-control-wireless-on-the-linux-desktop-with-these-tools #
	sudo nano /etc/network/interfaces
	#put this line for enable wireless#
	auto wlan0
	iface wlan0 inet static
        address 192.168.0.XXX   <--- your ip
        netmask 255.255.255.0   
        gateway 192.168.0.XXX     <--- your gateway
        wireless-essid XXXXXXX  <--- your SSID
        wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf

#configure ping test for probe#
	sudo nano /etc/rc.local
	#add this line before exit 0#
	/usr/bin/python /home/pi/Domotics-Raspberry/Software/Send_push_notification/round_robin_ping.py
	
#install RUBY#
	curl -L https://get.rvm.io | bash -s stable
	source /home/pi/.rvm/scripts/rvm
    rvm install ruby-2
	sudo chmod 777 /dev/i2c-0
	sudo chmod 777 /dev/i2c-1
	cd /home/pi/Domotics-Raspberry/domo.rb/
	gem 'wiringpi'
	bundle
	rackup
	#write test from client#
		 curl --data temp=2 192.168.0.202:9393/temperature/cucina
	#read test from client#
		curl 192.168.0.202:9292/temperature/cucina

#install webapi for python#
	#http://blog.luisrei.com/articles/flaskrest.html#
	sudo pip install flask
	
#enable thermo#
	/usr/bin/python /home/pi/Domotics-Raspberry/Software/thermo/thermo.py
	#check il you want push notification in the source code#
	
#enable server for push notification#
	python /Domotics-Raspberry/Software/Send_push_notification/Send_push.py
	
#VISUAL STUDIO 2010#
#Install redis client for c# #
#see the documentation https://github.com/ServiceStack/ServiceStack.Redis#


#if you want to test now the capability of your  powerful Raspberry go to

