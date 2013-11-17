#!/usr/bin/python
# -*- coding: utf-8 -*-
# mcp3008_lm35.py - read an LM35 on CH0 of an MCP3008 on a Raspberry Pi
# mostly nicked from
#  http://jeremyblythe.blogspot.ca/2012/09/raspberry-pi-hardware-spi-analog-inputs.html
 
import spidev
import time
import redis

#variable
server_redis = '192.168.0.205'
room_name = 'my room'
debug = False

spi = spidev.SpiDev()
spi.open(0, 0)

def readadc(adcnum):
	# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    adcout = ((r[1] & 3) << 8) + r[2]
    return adcout
 
i = 0
temp = 0.0
value = 0
vero = True
while vero:
    if i % 10 == 0 and i != 0:
        i = 0
		# transform to average value
        temp = temp / 10.0 
		# send to redis
        pool = redis.ConnectionPool(host=server_redis, port=6379, db=0)
        r = redis.Redis(connection_pool=pool)
        r.rpush(room_name,str(temp))
        temp = 0
        vero = False
	# read data from probe
    value = readadc(0)
	
    i +=1
    if debug:
        volts = (value * 3.3) / 1024
        temp += volts / (10.0 / 1000)
        print ("%4d/1023 => %5.3f V => %4.1f °C" % (value, volts,temp))
    time.sleep(0.2)
