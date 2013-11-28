#1 associate probe to rele
#2 read temperature probes
#3 read min-max temperature set
#4 if temperature < min activate rele
#5 if temperature > min deactivate rele


import time
import redis
room_name = 'my_room_2'

#variable
server_redis = '192.168.0.208'
pool = redis.ConnectionPool(host=server_redis, port=6379, db=0)
r = redis.Redis(connection_pool=pool)
print r.lrange(room_name,-1,-1).first()