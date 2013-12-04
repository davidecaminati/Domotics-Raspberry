import  pywapi
import string
import redis
import urllib2
import urllib
import time

#variable
server_redis = '192.168.0.208'
urlForNotification = 'http://192.168.0.208:5000/send_push/'
notification = True
message = ''


#print "Weather.com says: It is " + string.lower(weather_com_result['current_conditions']['text']) + " and " + weather_com_result['current_conditions']['temperature'] + "C now in Cesena.\n\n" + "icon is http://s.imwx.com/v.20131006.214956/img/wxicon/120/" +weather_com_result['current_conditions']['icon'] + ".png"

while True:
    #get weather
    weather_com_result = pywapi.get_weather_from_weather_com('ITAB1723')
    temp = string.lower(weather_com_result['current_conditions']['text'])
    cond = string.lower(weather_com_result['current_conditions']['temperature'])
    ico = "http://s.imwx.com/v.20131006.214956/img/wxicon/120/" + weather_com_result['current_conditions']['icon'] 
    
    pool = redis.ConnectionPool(host=server_redis, port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    r.rpush("current_temp_ext",str(temp))
    r.rpush("current_condition_ext",str(cond))
    r.rpush("current_ico_ext",str(ico))
    
    
    
    #message
    message = "fat fred!"
    notification = True
    
    if notification :
        msgToSend = urlForNotification + str(message) 
        NewmsgToSend = urllib.quote_plus(msgToSend)
        print NewmsgToSend
        res = urllib.urlopen(msgToSend)
        message= '' 
    time.sleep(30)