import sys,fcntl,os,time,struct
analog_addr = 0x6d
I2C_SLAVE   = 0x0703

#per la rev.A
#devname = "/dev/i2c-0"
#per la rev.B
devname = "/dev/i2c-1"

dev=os.open("/dev/i2c-1", os.O_RDWR)

fcntl.ioctl(dev, I2C_SLAVE, analog_addr)

for i in range(1): #there are 4 analog input
    cmd=bytearray([0x80 | 0x10 | (i<<5)])
    os.write(dev, cmd)
    time.sleep(0.004167)
    ret=os.read(dev, 2)
    mvolt=struct.unpack('>h',ret)[0]
    value = ((float(mvolt) - 1628.0) * 16.0) 
    print "mA: %s" % value
    

    