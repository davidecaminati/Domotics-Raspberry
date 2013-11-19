import smbus
import time
import redis
#variable
server_redis = '192.168.0.208' # IP of server redis (suggest to use the display TFT ip)
probe_name = 'windows_doors' # name in redis for this value
DEVICE = 0x24 # Device address (A0-A2)


r = redis.StrictRedis(host=server_redis, port=6379, db=0)

#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1


IODIRA = 0x00 # Pin direction register
GPIOA  = 0x12 # Register for inputs

# Set first 6 GPA pins as outputs and
# last one as input.
bus.write_byte_data(DEVICE,IODIRA,0x80)

# Loop until user presses CTRL-C
#while True:

  # Read state of GPIOA register
MySwitch = bus.read_byte_data(DEVICE,GPIOA)
  
#if MySwitch :
   #& 0b10000000 == 0b10000000:
   #print "Switch was pressed %s" % MySwitch
r.rpush(probe_name, MySwitch)
   #print r.lrange('finestre',0,-1)
   #time.sleep(1)
