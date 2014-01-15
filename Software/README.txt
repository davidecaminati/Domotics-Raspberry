Expand your partition, set password, set you timezone and keyboard, overclock to 800Mhz, i suggest to no start desktop mode (you need only the console mode) for fast boot then select finish for save and reboot.
#copy the repository# X
	git clone https://github.com/davidecaminati/Domotics-Raspberry

#start with an update# X
	sudo apt-get update  

#install REDIS (redis is a database)# X
	sudo apt-get install redis-server

#to use REDIS on Python# X
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
		
#SPI# X
	#Enabling the SPI kernel module#
	#As root, edit the kernel module blacklist file:#
		sudo nano /etc/modprobe.d/raspi-blacklist.conf

	#Comment out the spi-bcm2708 line so it looks like this:#
		#blacklist spi-bcm2708

	#Save the file so that the module will load on future reboots. To enable the module now, enter:#
			sudo modprobe spi-bcm2708

	#Now, if you run the lsmod command, you should see something like:#
		lsmod
		Module                  Size  Used by
		spi_bcm2708             4421  0
	#change permission permanent#
		sudo nano /etc/rc.local
		#add this two line before exit 0#
			sudo chmod 666 /dev/spidev0.0
			sudo chmod 666 /dev/spidev0.1
		
        [reboot]
        
#SPIDEV# X
	sudo apt-get install python-pip  
	sudo pip install spidev # error but continue  ???#
	sudo pip install python-dev
	sudo apt-get install python-imaging python-imaging-tk python-pip python-dev git
	mkdir python-spi
	cd python-spi
	wget https://raw.github.com/doceme/py-spidev/master/setup.py
	wget https://raw.github.com/doceme/py-spidev/master/spidev_module.c
	sudo python setup.py install
	cd ..
	sudo pip install wiringpi
	
#MODULE I2C# X
	sudo apt-get install python-smbus
	sudo apt-get install i2c-tools (usefull but not essential)
	sudo modprobe i2c-dev
	sudo modprobe i2c-bcm2708
	#change permission permanent#
		sudo nano /etc/rc.local
		#add this two line before exit 0#
			sudo chmod 666 /dev/i2c-0
			sudo chmod 666 /dev/i2c-1
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

#enable 1wire# X
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

            
#enable midori on Desktop#
	#set autostart#
		sudo nano /etc/xdg/lxsession/LXDE/autostart
		#write at the end of the file suggest to use 127.0.0.1 as IP-OF-YOUR_SERVER#		
			@midori -e Fullscreen -a http://127.0.0.1/mobile

	
#toggle light on the TFT#
	sudo nano /sys/class/backlight/fb_ili9320/bl_power
	#toggle 1 = (on) or 0 = (off)#

#configure web server# X
	sudo apt-get install apache2 php5 libapache2-mod-php5
	sudo rm /var/www/index.html
	sudo cp -r /home/pi/Domotics-Raspberry/Web_site/www/* /var/www/
	#set the redis server#
	

#configure analog probe(my_room_2)#
	#add the script to crontab#
	crontab -e
	#add at the end of the file#
	* * * * * /usr/bin/python /home/pi/Domotics-Raspberry/Hardware/Analog\ Temperature\ Probe/mcp3008_lm35.py
		 
#configure digital probe (my_room_1)#
	#add the script to crontab#
	crontab -e
	#add at the end of the file#
	* * * * * /usr/bin/python /home/pi/Domotics-Raspberry/Hardware/Digital\ Temperature\ Probe/thermometer.py
	#NOTE#
	#be sure to have activate 1 wire module otherwise look #enable 1wire# #

#configuration for read external temp from python# X
#link http://code.google.com/p/python-weather-api/#
#suggest to add this script in Display raspberry#
    sudo apt-get install subversion
	svn checkout http://python-weather-api.googlecode.com/svn/trunk/ python-weather-api-read-only
	 cd python-weather-api-read-only/
	 python setup.py build
	 sudo python setup.py install
	 crontab -e
	#add at the end of the file#
	* * * * * /usr/bin/python /home/pi/Domotics-Raspberry/Hardware/Display\ TFT/weather.py

#Update a device#
	#in Update directory, you will find usefull script to automate this (website, ....)#
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
        address 192.168.0.XXX   <--- your ippyth    
        netmask 255.255.255.0   
        gateway 192.168.0.XXX     <--- your gateway
        wireless-essid XXXXXXX  <--- your SSID
        wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf

#shutdown button#
#use pins 25,GND#
    sudo cp /home/pi/Domotics-Raspberry/Software/utility/turnoff.py /usr/local/bin/
    sudo chmod +x /usr/local/bin/turnoff.py
    sudo nano /etc/rc.local
    #add this line before exit 0#
			/usr/bin/python /usr/local/bin/turnoff.py &
            
#restart button#
#use pins 24,GND#
    sudo cp /home/pi/Domotics-Raspberry/Software/utility/restart.py /usr/local/bin/
    sudo chmod +x /usr/local/bin/restart.py
    sudo nano /etc/rc.local
    #add this line before exit 0#
			/usr/bin/python /usr/local/bin/restart.py &
	
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

#install webapi for python# X
	#http://blog.luisrei.com/articles/flaskrest.html#
	sudo apt-get install python-pip
	sudo pip install flask
	
#enable thermo control#
	/usr/bin/python /home/pi/Domotics-Raspberry/Software/thermo/thermo.py
	#check il you want push notification in the source code#
	
#enable COLOR LED control#
    sudo nano /etc/rc.local
	/usr/bin/python /home/pi/Domotics-Raspberry/Hardware/Color_LED/color_led.py

#enabled fade color led#
    #https://github.com/metachris/RPIO/blob/master/examples/example4_pwm_lowlevel.py#
    #http://pythonhosted.org/RPIO/pwm_py.html##
    #http://www.rpiblog.com/2012/11/pwm-on-raspberry-pi.html#
    sudo apt-get install git-core
    git clone git://git.drogon.net/wiringPi
    cd wiringPi/
    ./build
    # from https://github.com/metachris/RPIO#
    sudo easy_install -U RPIO

#enable server for push notification#
	#set autostart#
		sudo nano /etc/rc.local
		#add this line before exit 0#
			/usr/bin/python /home/pi/Domotics-Raspberry/Software/Send_push_notification/Send_push.py
	
#enable server and wall switch monitor for rele board control# X
	#set autostart#
		sudo nano /etc/rc.local
		#add this line before exit 0#
			/usr/bin/python /home/pi/Domotics-Raspberry/Hardware/Socket_to_MCP27013_con_i2c/rele_board_control.py &
			###OLD###/usr/bin/python /home/pi/Domotics-Raspberry/Hardware/Socket_to_MCP27013_con_i2c/read_pulse.py &
            ###/usr/bin/python /home/pi/Domotics-Raspberry/Hardware/Wall\ switch/wall_Switch.py &
		# for schema look at #
            http://fritzing.org/projects/rele-board-control-with-beedback-state-and-by-pass
			
#configure ping test for probe#
	#set autostart#
		sudo nano /etc/xdg/lxsession/LXDE/autostart
		#add this line at the end of the file#
			@/usr/bin/python /home/pi/Domotics-Raspberry/Software/Check_probe/check_probe.py
			
#configure door/windows monitor#
	#change permission permanent#
		sudo nano /etc/rc.local
		#add this two line before exit 0#
			sudo chmod 666 /dev/i2c-0
			sudo chmod 666 /dev/i2c-1
		#add the script to crontab#
		crontab -e
		#add at the end of the file#
			* * * * * /usr/bin/python /home/pi/Domotics-Raspberry/Hardware/Windows\ Switch\ MCP23017/windows_doors_probe.py

#Configure Webcam#
    sudo apt-get install python-imaging
    sudo pip install v4l2
            
            
#configure speek recognition on raspberry#
    #http://www.aonsquared.co.uk/raspi_voice_control#
    

#Configure XBEE#
#http://cae2100.wordpress.com/2012/12/23/raspberry-pi-and-the-serial-port/#
    sudo nano /etc/inittab
        #remark this line putting a # in front of the line#
        #T0:23:respawn:/sbin/getty -L ttyAMA0 115200 vt100 
    sudo nano  /boot/cmdline.txt
        #The contents of the file look like this#
        dwc_otg.lpm_enable=0 console=ttyAMA0,115200 kgdboc=ttyAMA0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait
        #Remove all references to ttyAMA0 (which is the name of the serial port). The file will now look like this#
        dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait
        sudo reboot
    #test serial port#
        sudo apt-get install minicom
        #Now run up minicom on the Raspberry Pi using#
        minicom -b 9600 -o -D /dev/ttyAMA0 
    #for python#
    #https://pypi.python.org/pypi/XBee#
        cd ~/Domotics-Raspberry/Hardware/XBEE/XBee-2.1.0
        sudo python setup.py install
        sudo pip install pyserial
    #http://jeffskinnerbox.wordpress.com/2013/01/30/configuration-utilities-for-xbee-radios/#
    #http://blog.james147.net/xbee-configuration/#
    #http://tutorial.cytron.com.my/2012/03/08/xbee-series-2-point-to-point-communication/#
        
#VISUAL STUDIO 2010#
#Install redis client for c# #
#see the documentation https://github.com/ServiceStack/ServiceStack.Redis#


#if you want to test now the capability of your powerful Raspberry go to

