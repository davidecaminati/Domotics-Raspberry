import  pywapi
import string
import redis
import urllib2
import urllib
import time

#variable
server_redis = '192.168.0.208'
urlForNotification = 'http://192.168.0.208:5000/send_push/'
notification = False
message = ''


#print "Weather.com says: It is " + string.lower(weather_com_result['current_conditions']['text']) + " and " + weather_com_result['current_conditions']['temperature'] + "C now in Cesena.\n\n" + "icon is http://s.imwx.com/v.20131006.214956/img/wxicon/120/" +weather_com_result['current_conditions']['icon'] + ".png"

while True:
    #get weather
    weather_com_result = pywapi.get_weather_from_weather_com('ITAB1723')
    temp = string.lower(weather_com_result['current_conditions']['temperature'])
    cond = string.lower(weather_com_result['current_conditions']['text'])
    ico = "http://s.imwx.com/v.20131006.214956/img/wxicon/120/" + weather_com_result['current_conditions']['icon'] + ".png"
    
    pool = redis.ConnectionPool(host=server_redis, port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    r.rpush("current_temp_ext",str(temp))
    r.rpush("current_condition_ext",str(cond))
    r.rpush("current_ico_ext",str(ico))
    
    
    
    #message
    message = "fat fred!"
    title = "temperatura" +  temp + " cond "  + cond 
    
    if notification :
        data = urllib.urlencode({'pushtext': str(message),'title': str(title)})
        req = urllib2.Request(urlForNotification,data)
        response = urllib2.urlopen(req)
        html = response.read()
        message= '' 
    time.sleep(100)