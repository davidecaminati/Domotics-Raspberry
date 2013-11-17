#configuration#
	nano mcp3008_lm35.py
	
	#set variable#
		server_redis = '192.168.0.205'   <--  your server redis ip
		room_name = 'my_room'            <--  name of room where the probe is (use single word, no space)

		#HOW check find correct name for room in redis db?#
		#open a redis terminal using command#
			redis-cli
		#tipicaly prompt is "redis 127.0.0.1:6379>"#
		#type this command to take the list of all field in redis database#
			KEYS *
		#if the response is (empty list or set) you can use every name you want for this room, otherwise#
		#you need to create a unique name (not already used)# 
		#NOTE: this field will be a list of value that store temperature of this room.#
		
		#enable debug#
			debug = True
		#this action allow to print the output in console during execution#
		
#test#
	sudo python mcp3008_lm35.py
	#be sure to have enabled the output (debug = True) to show the temperature in console.#

#schedule the push of data every 1 minute#
	crontab -e
	#go to the end of file and add this line#
	* * * * * sudo python /home/pi/Domotics-Raspberry/Hardware/Analog\ Temperature\ Probe/mcp3008_lm35.py
