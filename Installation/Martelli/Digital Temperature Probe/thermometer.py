import os 
import glob 
import time 
import redis

#variable
temp_um = "c"   # set "c" for celsius or "f" for fahrenheit
base_dir = '/sys/bus/w1/devices/' 
device_folder = glob.glob(base_dir + '28*')[0] 
device_file = device_folder + '/w1_slave' 
server_redis = '192.168.0.208'
room_name = 'my_room_1'
debug = True

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines 

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        if temp_um == "c":
            temp = "%.2f" % (float(temp_string) / 1000.0)
        else: # "f"
            temp = "%.2f" % (float(temp_string) / 1000.0 * 9.0 / 5.0 + 32.0)
        return temp

temp = read_temp()
pool = redis.ConnectionPool(host=server_redis, port=6379, db=0)
r = redis.Redis(connection_pool=pool)
r.rpush(room_name,str(temp))
if debug:
    print(temp)