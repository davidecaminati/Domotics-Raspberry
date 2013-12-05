#get address of the probes#
	 ls -l /sys/bus/w1/devices/
	 #return a list of device , you need file that start like 28-xxxxxxxxx#
	 #there are 1 file for each probe in the bus#

#install lib for perl#
	sudo apt-get install libwww-perl