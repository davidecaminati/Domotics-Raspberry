import smbus
import time
import redis
#variable
server_redis = '192.168.0.208' # IP of server redis (suggest to use the display TFT ip)
redis_probe_name = 'windows_doors_switch' # name in redis for this value
DEVICE = 0x24 # Device address (A0-A2)

r = redis.StrictRedis(host=server_redis, port=6379, db=0)
bus = smbus.SMBus(1) # Rev 2 Pi uses 1
IODIRA = 0x00 # Pin direction register
GPIOA  = 0x12 # Register for inputs

# Set pin
bus.write_byte_data(DEVICE,IODIRA,0x80)

# Read state of GPIOA register
MySwitch = bus.read_byte_data(DEVICE,GPIOA)

#if MySwitch :
   #& 0b10000000 == 0b10000000:

#write to redis
r.rpush(redis_probe_name, MySwitch)
