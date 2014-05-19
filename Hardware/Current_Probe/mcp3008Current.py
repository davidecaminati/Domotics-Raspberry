#!/usr/bin/python
# -*- coding: utf-8 -*-
# mcp3008Current.py - read an SCT013 on CH0 of an MCP3008 on a Raspberry Pi
# mostly nicked from
#  http://jeremyblythe.blogspot.ca/2012/09/raspberry-pi-hardware-spi-analog-inputs.html

import spidev
import time
debug = True

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
amps = 0.0
value = 0
vero = True
while vero:
    if i % 1000 == 0 and i != 0:
        val = abs(amps/1000.0 - 1022.0)
        if val > 40:
            print "%s W" % int((40 + 3 * (val -40)))
        else:
            print "%s W" % int((val * 1.5))
        amps = 0
        i = 0
    value = readadc(0)
    amps += value
    i +=1
