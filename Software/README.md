## Domotics project


### OS Initial configuration
* Expand your partition
* Set password
* Set you timezone and keyboard
* Overclock to 800Mhz
* Select finish for save and reboot

I suggest to **not start desktop mode** (you need only the console mode) for fast boot. 


### Copy the repository
git clone https://github.com/davidecaminati/Domotics-Raspberry


### Update the system
sudo apt-get update  

### Install REDIS 
```ruby
# install latest redis-server 
sudo apt-get install redis-server
	
#Configure binding	
sudo nano /etc/redis/redis.conf
# remark bind 127.0.0.1 putting a # infront of the line
bind 127.0.0.1
```

### REDIS on Python
```ruby
sudo apt-get install python-setuptools
sudo easy_install redis
```
	
### REDIS on PHP
```ruby
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
```

### Enable SPI module
```ruby
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
```

### SPIDEV
```ruby
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
```
	
### Enable I2C module
```ruby
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
```

### Enable 1wire module
```ruby
sudo nano /etc/modules
#add this lines#
w1-gpio
w1-therm
```
	
### Send keys
```ruby
#http://tjjr.fi/sw/python-uinput/#download-and-install#
sudo pip install evdev
sudo pip install python-uinput
```
    
### Enable TFT display
```ruby
#guide http://www.raspberrypi.org/phpBB3/viewtopic.php?f=64&t=48967#
#model http://www.raspberrypi.org/phpBB3/viewtopic.php?f=59&t=48956#

sudo wget https://raw.github.com/Hexxeh/rpi-update/master/rpi-update -O /usr/bin/rpi-update && sudo chmod +x /usr/bin/rpi-update

#sudo mv /lib/modules/$(uname -r) /lib/modules/$(uname -r).bak
sudo cp -R /lib/modules/$(uname -r) /lib/modules/$(uname -r).bak

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

#sudo apt-get update	
sudo apt-get install libts-bin evtest xinput
sudo pip install evdev

#To calibrate the touch panel#
sudo TSLIB_FBDEVICE=/dev/fb1 TSLIB_TSDEVICE=/dev/input/event0 ts_calibrate


######UPDATE for image 2014-01-07-wheezy-raspbian-2014-03-12-fbtft-hy28a.img ###
#if you need to rotate the screen on the TFT touch 2,8 "#
sudo nano /boot/cmdline.txt
#change fbtft_device.rotate=270 with fbtft_device.rotate=90 #
sudo nano  /etc/X11/xorg.conf.d/99-calibration.conf
#edit the file like this#
Section "InputClass"
    Identifier      "calibration"
    MatchProduct    "ADS7846 Touchscreen"
    Option  "SwapAxes"      "1"
    Option "InvertX" "True"
EndSection

Section "InputClass"
    Identifier      "calibration"
    MatchProduct    "stmpe-ts"
    Option  "SwapAxes"      "1"
    Option "InvertX" "True"
EndSection

#if you need to disable suspend add this#
Section "ServerFlags"
    Option         "blank time" "0"
    Option         "standby time" "0"
    Option         "suspend time" "0"
    Option         "off time" "0"
EndSection
#edit this file for touchscreen#
sudo nano /usr/share/X11/xorg.conf.d/10-evdev.conf
#addthis line on each input class (probably is necessary only for touchscreen)#
Option "InvertY" "True"

#remove suspend#
sudo nano  /etc/X11/xorg.conf.d/99-calibration.conf
#add this part in the end of the file#
Section "ServerFlags"
    Option         "blank time" "0"
    Option         "standby time" "0"
    Option         "suspend time" "0"
    Option         "off time" "0"
EndSection
```

### Api temperature for request temperature to redis server
```ruby
sudo nano /etc/rc.local
#add this line before exit 0#
/usr/bin/python /home/pi/Domotics-Raspberry/Software/Weather/api_temperature.py &
```

		
### Enable midori on TFT
```ruby
sudo nano /boot/cmdline.txt
#at the end of line add this#
fbcon=map:10 fbcon=font:VGA8x8
#set autostart#
sudo nano /etc/xdg/lxsession/LXDE/autostart
#write at the end of the file suggest to use 127.0.0.1 as IP-OF-YOUR_SERVER#		
@xset s off
@xset -dpms
@xset s noblank
@midori -e Fullscreen -a http://127.0.0.1
# if necessary  comment out the @xscreensaver line with a #
```
    
#Disable mouse cursor
```ruby
sudo nano /etc/X11/xinit/xserverrc
#add -nocursor as parameter#
exec /usr/bin/X -nocursor -nolisten tcp "$@"
```

#Auto startx: modify this file
```ruby
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

#enable desktop manager on raspi-config
sudo raspi-config
#select enable desktop manager

#reboot#
sudo reboot
```
>if problems look https://learn.adafruit.com/adafruit-pitft-28-inch-resistive-touchscreen-display-raspberry-pi/touchscreen-install-and-calibrate#
            
### enable midori on Desktop
```ruby
#set autostart#
sudo nano /etc/xdg/lxsession/LXDE/autostart
#write at the end of the file suggest to use 127.0.0.1 as IP-OF-YOUR_SERVER#		
@midori -e Fullscreen -a http://127.0.0.1/mobile
```

### Toggle light on the TFT
```ruby
sudo nano /sys/class/backlight/fb_ili9320/bl_power
#toggle 1 = (on) or 0 = (off)#
```

### Configure web server old version PHP
```ruby
sudo apt-get install apache2 php5 libapache2-mod-php5
sudo rm /var/www/index.html
sudo cp -r /home/pi/Domotics-Raspberry/Web_site/www/* /var/www/
#set the redis server#
```
    
    
### Configure web server NEW version HTML5
```ruby
sudo apt-get install apache2 php5 libapache2-mod-php5
sudo rm /var/www/index.html
sudo cp -r /home/pi/Domotics-Raspberry/Web_site_NEW/* /var/www/
#set the redis server#
```
	
### Installation Servos driver
```ruby
git clone https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git
#to start the example#
#Note default address is 40, use "i2cdetect -y 1" to detect your, don't warry about the address 70#
cd Adafruit-Raspberry-Pi-Python-Code/
cd Adafruit_PWM_Servo_Driver/
sudo python Servo_Example.py
```
> reference http://learn.adafruit.com/downloads/pdf/adafruit-16-channel-servo-driver-with-raspberry-pi.pdf
    
### Configure analog probe(my_room_2)
```ruby
#add the script to crontab#
crontab -e
#add at the end of the file#
* * * * * /usr/bin/python /home/pi/Domotics-Raspberry/Hardware/Analog\ Temperature\ Probe/mcp3008_lm35.py
```

### Configure digital probe (my_room_1)
```ruby
#add the script to crontab#
crontab -e
#add at the end of the file#
* * * * * /usr/bin/python /home/pi/Domotics-Raspberry/Hardware/Digital\ Temperature\ Probe/thermometer.py
#NOTE#
#be sure to have activate 1 wire module otherwise look #enable 1wire# 
```

> configuration for read external temp from python
> link http://code.google.com/p/python-weather-api/
> suggest to add this script in Display raspberry

    sudo apt-get install subversion
	svn checkout http://python-weather-api.googlecode.com/svn/trunk/ python-weather-api-read-only
	cd python-weather-api-read-only/
	python setup.py build
	sudo python setup.py install
	crontab -e
	#add at the end of the file#
	* * * * * /usr/bin/python /home/pi/Domotics-Raspberry/Software/Weather/weather.py

### Update a device
> in Update directory, you will find usefull script to automate this (website, ....)
	cd /home/pi/Domotics-Raspberry/Update
	
###Error in editing file from windows
	>if you need to create a  new bash script from windows , pay attention to new line characters , in Win are different than unix
	>so if you want to sure your file are compatible , you coud install an utility to convert file in unix style
		sudo apt-get install dos2unix
		#how to use this utility#
		dos2unix <file to convert>
		
### Configure wireless
> for help http://www.linux.com/learn/tutorials/374514-control-wireless-on-the-linux-desktop-with-these-tools 
	sudo nano /etc/network/interfaces
	#put this line for enable wireless#
	auto wlan0
	iface wlan0 inet static
        address 192.168.0.XXX   <--- your ippyth    
        netmask 255.255.255.0   
        gateway 192.168.0.XXX     <--- your gateway
        wireless-essid XXXXXXX  <--- your SSID
        wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf

### Shutdown button
> use pins 25,GND
    sudo cp /home/pi/Domotics-Raspberry/Software/utility/turnoff.py /usr/local/bin/
    sudo chmod +x /usr/local/bin/turnoff.py
    sudo nano /etc/rc.local
    #add this line before exit 0#
			/usr/bin/python /usr/local/bin/turnoff.py &
            
### Restart button
> use pins 24,GND
    sudo cp /home/pi/Domotics-Raspberry/Software/utility/restart.py /usr/local/bin/
    sudo chmod +x /usr/local/bin/restart.py
    sudo nano /etc/rc.local
    #add this line before exit 0#
			/usr/bin/python /usr/local/bin/restart.py &
	
### Install RUBY
	curl -L https://get.rvm.io | bash -s stable
	source /home/pi/.rvm/scripts/rvm
    rvm install ruby-2
	sudo chmod 777 /dev/i2c-0
	sudo chmod 777 /dev/i2c-1
	cd /home/pi/Domotics-Raspberry/domo.rb/
	gem 'wiringpi'
	bundle
	rackup
	>write test from client
		 curl --data temp=2 192.168.0.202:9393/temperature/cucina
	>read test from client
		curl 192.168.0.202:9292/temperature/cucina

### Install webapi for python
	#http://blog.luisrei.com/articles/flaskrest.html#
	sudo apt-get install python-pip
	sudo pip install flask
	
### Enable thermo control
	/usr/bin/python /home/pi/Domotics-Raspberry/Software/thermo/thermo.py
	#check il you want push notification in the source code#
	
### Enable COLOR LED control
    sudo nano /etc/rc.local
	/usr/bin/python /home/pi/Domotics-Raspberry/Hardware/Color_LED/color_led.py

### Enabled fade color led
    #https://github.com/metachris/RPIO/blob/master/examples/example4_pwm_lowlevel.py#
    #http://pythonhosted.org/RPIO/pwm_py.html##
    #http://www.rpiblog.com/2012/11/pwm-on-raspberry-pi.html#
    sudo apt-get install git-core
    git clone git://git.drogon.net/wiringPi
    cd wiringPi/
    ./build
    # from https://github.com/metachris/RPIO#
    sudo easy_install -U RPIO

### Enable server for push notification
	#set autostart#
		sudo nano /etc/rc.local
		#add this line before exit 0#
			/usr/bin/python /home/pi/Domotics-Raspberry/Software/Send_push_notification/Send_push.py
	
### Enable server and wall switch monitor for rele board control
	sudo pip install pyserial
	--- required this setup--> #Configure XBEE#
	>set autostart
		sudo nano /etc/rc.local
		>add this line before exit 0
			/usr/bin/python /home/pi/Domotics-Raspberry/Hardware/Socket_to_MCP27013_con_i2c/rele_board_control.py &
			###OLD###/usr/bin/python /home/pi/Domotics-Raspberry/Hardware/Socket_to_MCP27013_con_i2c/read_pulse.py &
            ###/usr/bin/python /home/pi/Domotics-Raspberry/Hardware/Wall\ switch/wall_Switch.py &
		> for schema look at 
            http://fritzing.org/projects/rele-board-control-with-beedback-state-and-by-pass
			
### Configure ping test for probe
	>set autostart
		sudo nano /etc/xdg/lxsession/LXDE/autostart
		#add this line at the end of the file#
			@/usr/bin/python /home/pi/Domotics-Raspberry/Software/Check_probe/check_probe.py
			
### Configure door/windows monitor
	#change permission permanent#
		sudo nano /etc/rc.local
		#add this two line before exit 0#
			sudo chmod 666 /dev/i2c-0
			sudo chmod 666 /dev/i2c-1
		#add the script to crontab#
		crontab -e
		#add at the end of the file#
			* * * * * /usr/bin/python /home/pi/Domotics-Raspberry/Hardware/Windows\ Switch\ MCP23017/windows_doors_probe.py

### Configure Webcam
    sudo apt-get install python-imaging
    sudo pip install v4l2
            
            
### Configure speek recognition on raspberry
    #http://www.aonsquared.co.uk/raspi_voice_control#
    

### Configure XBEE
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
        
### VISUAL STUDIO 2010
#Install redis client for c# #
#see the documentation https://github.com/ServiceStack/ServiceStack.Redis#


### Enable Nokia 5110 Display (SPI interface)
	git clone git://git.drogon.net/wiringPi
	cd wiringPi
	./build
	sudo apt-get install python-dev python-imaging python-imaging-tk python-pip
	sudo pip install wiringpi wiringpi2
	cd 
	sudo nano /etc/modprobe.d/raspi-blacklist.conf
	#make sure have enabled SPI module adding a # at the init of the line #
		#blacklist spi-bcm2708
	git clone https://github.com/XavierBerger/pcd8544.git
	cd pcd8544
	./setup.py clean build
	sudo ./setup.py install
	cd examples
	sudo python dimmer.py 


### Enable PiCamera
	sudo apt-get update
	sudo pip install picamera
	sudo apt-get install python-picamera
	#to test#
		raspistill -o cat.jpg -t 10000
	#if you receive this error#
		mmal: Failed to run camera app. Please check for firmware updates
		#you need to:#
		#set 256 MB of ram in your video card using rasp-config#
		#check this 2 file#
		sudo nano /etc/modprobe.d/raspi-blacklist.conf
			blacklist spi-bcm2708
			blacklist i2c-bcm2708

		sudo nano /etc/modules 
			w1-therm
			w1-gpio pullup=1
			i2c-dev
			i2c-bcm2708
			spi-bcm2708
			snd-bcm2835
			bcm2708_wdog
			
# start on boot up#
#Here is the command line info and file contents:#

	nano RunCamera.sh

	#! /bin/bash
	python /home/pi/CamInterface.py

	chmod +x RunCamera.sh
	sudo nano /etc/init.d/StartCameraInterface.sh

	#! /bin/bash
	# /etc/init.d/StartCameraInterface.sh
	
	### BEGIN INIT INFO
	# Provides: Starts Camera interface at startup
	# Required-Start: $remote_fs $syslog
	# Required-Stop: $remote_fs $syslog
	# Default-Start: 2 3 4 5
	# Default-Stop: 0 1 6
	# Short-Description: Simple script to start a program at boot
	# Description: A simple script from www.stuffaboutcode.com which will start / stop a program a boot / shutdown.
	### END INIT INFO
	
	# If you want a command to always run, put it here
	# Carry out specific functions when asked to by the system
	case �$1? in
	start)
	echo �Starting Camera Interface�
	# run application you want to start
	/home/pi/RunCamera.sh
	;;
	stop)
	echo �Stopping Camera Interface�
	# kill application you want to stop
	killall RunCamera.sh
	kill $(ps aux | grep �python /home/pi/CamInterface.py� | awk �{ print $2 }�)
	;;
	*)
	
	echo �Usage: /etc/init.d/noip {start|stop}�
	exit 1
	;;
	esac
	
	exit 0
    
	sudo chmod 755 /etc/init.d/StartCameraInterface.sh
	sudo update-rc.d StartCameraInterface.sh defaults
	sudo reboot
	

### Bluetooth Proximity
    #install bluetooth software#
    #http://rasspberrypi.wordpress.com/2012/09/03/install-bluetooth-dongle-on-raspberry-pi/#
    sudo apt-get update
    sudo apt-get install bluetooth
    1. On boot i typed the following command to see if my connected dongle was visible.
    $lsusb

    This returned the following line to make sure that the dongle was detected
    Bus 001 Device 004: ID 1131:1001 Integrated System Solution Corp. KY-BT100 Bluetooth Adapter

    2. Then typed in
    $lsmod

    This returned
    bluetooth 166552 23 btusb,rfcomm,bnep

    3. Now to install bluetooth package
    $sudo apt-get install bluetooth

    Note: Installation takes a while relax and enjoy for the time

    4. Now after the installation is completed, run the following to get the status.
    $/etc/init.d/bluetooth status

    This is returned if all is good
    [ ok ] bluetooth is running.

    5. Now you can find your blueetooth address using the following command
    $hcitool dev

    This returns something like this
    Devices:
    hci0 00:11:67:10:80:F0

    6. Now we can scan for nearby devices using the following command
    $hcitool scan

    This returns
    Scanning ...
    54:9B:12:99:36:61 YourBluetoothDevice

    7. Now we can run a small test to connect to the following device
    $sudo l2ping -c 1 54:9B:12:99:36:61

    This returns
    Ping: 54:9B:12:99:36:61 from 00:11:67:10:80:F0 (data size 44) ...
    0 bytes from 54:9B:12:99:36:61 id 0 time 19.28ms
    1 sent, 1 received, 0% loss

    Success :)
    
    
    #now#
    apt-get install bluetooth bluez-utils
    
    
    
    
    
    #now install the utility software#
    sudo apt-get install blueproximity
    #For security reasons, some interactions with the mobile require that the device is `paired' with the one it is interacting with. First, store a number (4 or more digits) in the file /etc/bluetooth/pin (say 12345). Stop and restart the bluetooth service by doing:
        sh /etc/init.d/bluetooth stop
        sh /etc/init.d/bluetooth start
    #make discoverable raspberry bluetooth#
    sudo hciconfig hci0 piscan
    #Setup bluetooth-agent to pass the expected pairing code#
    #install tools#
    sudo apt-get install bluez-tools
    #script#
    sudo rfcomm connect 0 B0:EC:71:72:FF:8D
    watch -n 0.5 hcitool  rssi B0:EC:71:72:FF:8D


### Sound Control the volume adjuster
    #this software permit to control the main volume of a Windows 7 64bit using a raspberry and a microphone near the loudspeackers#
        #for windows#
            #launch the exe file located in SimpleWebServer#
            #path Software\SimpleWebServer\SimpleWebServer\bin\Debug\SimpleWebServer.exe#
            #copy this file in a folder of your Windows computer#
            #download this program nircmd from this url http://www.nirsoft.net/utils/nircmd.html  (bottom of the page)#
            #put nircmd.exe in the same folder of the SimpleWebServer.exe#
            #run SimpleWebServer.exe#
            
        #for Raspberry#
            #NOTE, i use a usb audio interface for mic input#
            sudo apt-get install python-pyaudio
            #execute the program#
            python  /home/pi/Domotics-Raspberry/Software/VolumeControl/volumeControl.py
            
### Audio multiroom with graphic control
	#download the image 2014-01-07-wheezy-raspbian-2014-03-12-fbtft-hy28a.img # 
	#url for download http://tronnes.org/downloads/2014-01-07-wheezy-raspbian-2014-03-12-fbtft-hy28a.zip#
	#unzip and copy the image file into SDCARD using Win32DiskImager.exe#
	#boot and wait the prompt (is normal 1 auto reboot for configuration)#
	#login with user pi password raspberry#
	#change the password# i use "1"#
		sudo passwd pi
	#update#
		sudo apt-get update
	#Install audio-related packages needed by SoundWire (Pulse Audio, Pulse Audio Volume Control, Portaudio)#
        sudo apt-get install -y pulseaudio pavucontrol libportaudio2
    #Launch Pulse Audio Volume Control, needs the GUI (X Windows) running.#
		#if you are connected througt SSH client need to export the display using this command
			export DISLPAY=:0
		#launch the graphical interface#
			startx
			#aligh the touchscreen with a pencil pressing the cross on the screen#
		#start another ssh session using PUTTY#
		#download the server for Raspberry#
			wget http://georgielabs.99k.org/SoundWire_Server_RPi.tar.gz
		#uncompress the file#
			tar xvzf SoundWire_Server_RPi.tar.gz
		#move to the folder#
			cd SoundWireServer/
		#make executable the program#
			sudo chmod +x SoundWireServer
		#using winscp (ssh graphical interface, copy some mp3 in the home folder of pi user (/home/pi)#
		#install mpg123 (mpeg player)#
			sudo apt-get install mpg123
		#launch SoundWireServer#
			./SoundWireServer
        #open pavucontrol on the display of raspberry#
            export DISPLAY=:0
            pavucontrol
            #go in the tab [Configuration]#
            #select Profile [OFF] (this is to fix the error of mp3 session still running after close)#
        #close the graphical interface ([ctrl]+c) in the other PUTTY session.
        #go in the folder of executable server#
            cd ~/SoundWireServer
        #restart the server#
            ./SoundWireServer
		#open another ssh client PUTTY#
		#launch mp3 player with a song#
			mpg123 name_of_mp3
	#Install demon for control mp3 with API#
        sudo pip install flask
        ######NEED A PROCEDURE#####
        ### need to start SoundWireServer and python script  AS USER NON ROOT ####
            sudo nano /etc/rc.local
            #add this line before exit 0#
            (sleep 5;su - pi -c "/usr/bin/python /home/pi/Domotics-Raspberry/Software/RadioStreaming/radioStreaming.py ")&

    #install SoundWire on your Android Phone from the market#
		#connect the SoundWire client to your server putting the address in the text box (ex. 192.168.0.208)
    
### API for redis server interface and Streaming server interface
    sudo nano /etc/rc.local
		#write at the end of the file #		
		(sleep 5;su - pi -c "/usr/bin/python /home/pi/Domotics-Raspberry/Software/RadioStreaming/radioStreaming.py ")&

        
### Streaming Audio server (SoundWire)
    #install prerequisite#
    sudo apt-get install pavucontrol
    sudo apt-get install pulseaudio
    sudo apt-get install mpg123
    #download the server#
        wget http://georgielabs.99k.org/SoundWire_Server_RPi.tar.gz
    #extract#
        tar -zxvf SoundWire_Server_RPi.tar.gz
        cd SoundWireServer
    #1) Start the SoundWire Server application from the command line:
      ./SoundWireServer &
    #The first time you do this you should have the GUI running (X Windows) so that
    #you can launch Pulse Audio Volume Control later below.
    #SoundWireServer will display the IP address (IPv4) of the server, or several
    #addresses if there's more than one possibility. You should see the message
    #"Audio capture running". If not then there is a problem, check the other output
    #lines for details. To see the complete console output start SoundWireServer with
    #the -verbose option, this will display messages from Portaudio.
    #
    #2) Launch Pulse Audio Volume Control, needs the GUI (X Windows) running.
        #pavucontrol &
    #If it doesn't start then it may not be installed, or pavucontrol may not be in
    #your search path. You can also start it from your GUI. If you have no GUI then 
    #you should configure pulse audio as required manually if SoundWire doesn't work.
    #
    #3) In Pulse Audio Volume Control go to the Configuration tab, select Internal
    #Audio profile "Analog Stereo Duplex" or a similar name. Alternatively, try
    #different configuration profiles if you have problems. SoundWire can also work
    #with no audio hardware present, in which case the Configuration tab may be
    #empty. You can also simulate having no audio hardware by selecting profile
    #"Off", SoundWire should still work properly by monitoring Pulse's dummy output.
    ##USE OFF#
    #in case of problem read the README file inside the directory of Soundwire#
    sudo nano /etc/rc.local
        #write at the end of the file #		
        su -l pi -c " ./SoundWireServer/SoundWireServer &"
    #NOTE#
    #you need to copy some mp3 in /home/pi/mp3/ folder with name 1.mp3, 2.mp3 .....

### Read tag ID3 from python
#for information http://eyed3.nicfit.net/installation.html#
    sudo pip install eyeD3
    #this is the code#
    
    import eyed3
    audiofile = eyed3.load("/home/pi/mp3/1.mp3")
    print audiofile.tag.artist
    print audiofile.tag.album 
    print audiofile.tag.title 
    print audiofile.tag.track_num

    
### Read process list and CPU usage
#for information https://github.com/giampaolo/psutil#
    sudo apt-get install python-psutil
    #for documentation https://pypi.python.org/pypi/psutil# 
        # # exceptions
        "Error", "NoSuchProcess", "AccessDenied", "TimeoutExpired",
        # constants
        "NUM_CPUS", "TOTAL_PHYMEM", "BOOT_TIME",
        "version_info", "__version__",
        "STATUS_RUNNING", "STATUS_IDLE", "STATUS_SLEEPING", "STATUS_DISK_SLEEP",
        "STATUS_STOPPED", "STATUS_TRACING_STOP", "STATUS_ZOMBIE", "STATUS_DEAD",
        "STATUS_WAKING", "STATUS_LOCKED",
        # classes
        "Process", "Popen",
        # functions
        "test", "pid_exists", "get_pid_list", "process_iter", "get_process_list",
        "phymem_usage", "virtmem_usage"
        "cpu_times", "cpu_percent", "per_cpu_percent",
        "network_io_counters", "disk_io_counters",

### Wolframalpha integration#
    #http://www.wolframalpha.com/input/?i=tomorrow+temperature+cesena+italy
    
### Configuration for webapi on Windows 7 64 bit computer (probably works on all windows systems
    #install python 2.7 from this url https://www.python.org/ftp/python/2.7.6/python-2.7.6.msi#
        #open prompt MSDOS#
        #copy the file [your download path]/Domotics-Raspberry/Software/Windows7/distribute_setup.py in c:/distribute_setup.py
        #go in the installation directory of python (ex. c:\python27\ )
        #launch "python.exe c:\distribute_setup.py"
        #go in the folder SCRIPTS (cd scripts)#
        #launch "easy_install.exe flask" for install flask framework#
        #close Prompt MSDOS#
        #copy [your download path]/Domotics-Raspberry/Software/Windows7/avvioWebApi.bat in C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup/avvioWebApi.bat#
        #copy [your download path]/Domotics-Raspberry/Software/Windows7/webservice.bat in c:/webservice.bat#
        
### Minix X5 mini for speek engine
    #install on the minix this software#
    SSHDroid (ssh server)
    SL4A Script Launcher 
    TaskBomb task scheduler
    #run Script Launcher#
        #click on the link SL4A and go in the download page, in the left download the first link Python4Android_r4.apk and the link sl4a_r6.apk#
        #download and install Python4Android_r4.apk#
        #download and install sl4a_r6.apk#
        #after the installation , open Python4Android and click on the first button [INSTALL] (start the download of PythonExtra_14)#
        #select [Browse Module] then click on TWISTEDmatrix for download it (dont try to install, this is an EGG file not APK)#
        #return in [IMPORT MODULES] then select TWISTEDmatrix for import the module#
    #from a computer download and unzip lastest CherryPy from this url https://pypi.python.org/pypi/CherryPy/3.2.4#
        #copy the folder (in my case using winscp because i'm on Windows machine)  (ex /home/pi/CherryPy-3.2.4 in a Raspberry (we need linux for compile this with ARM architecture#
        #open ssh on this raspberry, go in the folder /home/pi/CherryPy-3.2.4#
        #launch this command python setup.py build#
        #now you have created lib.linux-armv6l-2.7 folder inside the build folder#
        #copy build folder in a folder of your pc (ex c:\cherrypy\build)#
    #in the android pc (MINIX) run SSHDroid to have SSH access#
        #open ssh session from yout PC to MINX pc#
        #move to folder /sdcard/sl4a/scripts for check if exist#
        #now copy (with WINSCP) the folder cherrypy (c:\cherrypy\build\lib.linux-armv6l-2.7\cherrypy)  into MINIX /sdcard/sl4a/scripts
        # for more information look http://www.defuze.org/archives/228-running-cherrypy-on-android-with-sl4a.html#
    #create a new file in /sdcard/sl4a/scripts named cpdroid.py#
        #put inside the new file ([repository]/Domotics-Raspberry/trunk/Software/Android/Minix/cpdroid.py) this code#
    #open the launcher and click on the cpdroid.py file to start the server#
    #add translation module for python#
        #download Goslate from https://pypi.python.org/pypi/goslate#downloads#
        #put this file into Minix in the folder /mnt/sdcard/Download#
        #open Python for Android, press [Import Modules] then select goslate#
       

    SL4A
    QPython - Python for Android
    
### Nota per avvio automatico
    root@raspberrypi:~/shairport# make install
    root@raspberrypi:~/shairport# cp shairport.init.sample /etc/init.d/shairport
    root@raspberrypi:~/shairport# cd /etc/init.d
    root@raspberrypi:/etc/init.d# chmod a+x shairport
    root@raspberrypi:/etc/init.d# update-rc.d shairport defaults

    
### DATE ISSUE
    #chenge the file#
    sudo nano /etc/resolv.conf
    #add this line#
    nameserver 8.8.8.8
    nameserver 8.8.4.4
    #if not work open the file#
    sudo nano /etc/network/interfaces
    #above the line#
    iface eth0 inet dhcp
    #you need to insert#
    dns-nameserver 8.8.8.8
    #restart the daemon#
    service ntpd restart
    #or#
    /etc/init.d/ntpd restart
    #use the command  "date" to test.#
    date

#if you want to test now the capability of your powerful Raspberry go to

