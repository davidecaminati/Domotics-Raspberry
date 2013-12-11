#!/usr/bin/env python3

import sys,fcntl,os,time,struct
from collections import Counter
analog_addr = 0x6d
I2C_SLAVE   = 0x0703

#per la rev.A
#devname = "/dev/i2c-0"
#per la rev.B
devname = "/dev/i2c-1"

dev=os.open("/dev/i2c-1", os.O_RDWR)

fcntl.ioctl(dev, I2C_SLAVE, analog_addr)

while True:
    valore = 0
    for x in range(50):
        valori = []
        for i in range(10):
                cmd=bytearray([0x80 | 0x10 | (0<<5)])
                os.write(dev, cmd)
                time.sleep(0.004167)
                ret=os.read(dev, 2)
                mvolt=struct.unpack('>h',ret)[0]
                #valore = ((float(mvolt) - 1628.0) * 16.0) #continua
                valore = ((float(mvolt) - 1628.0) ) 
                
                valori.append(valore)
                #print("{}mV".format(mvolt))
                #print "mA: %f" % valore
    
        def moda(valori):
            ricorrenza = Counter(valori).most_common(1)  
            
            return ricorrenza
        ric = moda(valori)
        milliamper = ric[0][0]
        watt = (milliamper/ 1000.0) * 0.3
        if valore < watt:
            valore = watt
    print ric
    for i in range(4):
            cmd=bytearray([0x80 | 0x1c | (i<<5)])
            os.write(dev, cmd)
            time.sleep(0.67)
            ret=os.read(dev, 4)
            value=struct.unpack('>l',ret)[0]
            uvolt=uvolt=(value >> 8) * 1000 / 64
    
            print("{}uV".format(uvolt))