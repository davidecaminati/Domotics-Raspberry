#set file as executable#
	chmod +x 01_read_temp.sh
	chmod +x 05_memorizza_temp.sh 
	chmod +x 06_display_letture.sh
	

#get address of the probes#
	 ls -l /sys/bus/w1/devices/
	 #return a list of device , you need file that start like 28-xxxxxxxxx#
	 #there are 1 file for each probe in the bus#
	 copy the name of the file like 28-xxxxxxxxxxx and paste in the variable in 01_read_temp.sh (es 28-0000047b16f9)
	
#set variable#
	nano 01_read_temp.sh
	sensors[0]='28-0000047b16f9'    <--- set your probe ID
	sensors[1]='28-0000047b16f9'    <--- set your second probe ID if exist else remark the line with #
	
#install lib for perl#
	sudo apt-get install libwww-perl