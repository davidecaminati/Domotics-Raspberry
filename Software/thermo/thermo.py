#1 associate probe to rele
#2 read temperature probes
#3 read min-max day/night temperature set (day 6-20, night 20-6)

#4 if temperature < min activate rele
#5 if temperature > min deactivate rele


import time
import redis
import urllib2


room_name = 'my_room_1'

#variable
server_redis = '192.168.0.208'
temp_min_night = "t_min_night"
temp_max_night = "t_max_night"
temp_min_day = "t_min_day"
temp_max_day = "t_max_day"
MinTemp = 10
MaxTemp = 20
ActualTemp = 15
urlOn = 'http://192.168.0.202:5000/releon/1'
urlOff = 'http://192.168.0.202:5000/releoff/1'
urlForNotification = 'http://192.168.0.202:5000/push/'
notification = False
status = ''

while True:
    pool = redis.ConnectionPool(host=server_redis, port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    ActualTemp = r.lrange(room_name,-1,-1)[0]
    #get time
    current_hour = time.strptime(time.ctime(time.time())).tm_hour
    if current_hour < 6 or  current_hour > 20:
        MinTemp = r.get(temp_min_night)
        MaxTemp = r.get(temp_max_night)
    else:
        MinTemp = r.get(temp_min_day)
        MaxTemp = r.get(temp_max_day)
    
    if MinTemp > ActualTemp:
        #start rele
        res = urllib2.urlopen(urlOn)
        status = res.read()
    elif ActualTemp > MaxTemp :
        #stop rele
        res = urllib2.urlopen(urlOff)
        status = res.read()

    if notification and status != '':
        res = urllib2.urlopen(urlForNotification + str(status))
    status = ''
    time.sleep(10)
    