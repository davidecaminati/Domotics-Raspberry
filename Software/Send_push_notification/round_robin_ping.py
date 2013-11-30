import httplib, urllib 
import subprocess 
import time
import urllib
import urllib2

#205 digital probe
#208 monitor TFT  server web
#86 PC windows
#202 rele
#211 analog Probe
ip_device_list = [202,211,208,205] 
ip_device_list_Error = []
urlForNotification = 'http://192.168.0.208:5000/send_push/'
while True:
    for ping in ip_device_list:
        print ip_device_list
        print ip_device_list_Error
        if (ping in ip_device_list_Error) == False:
            address = "192.168.0." + str(ping)
            res = subprocess.call(['ping', '-c', '1', address])
            if res == 0:
                print "ping to", address, "OK "
            else:
                print "no response from", address
                message = "error from  %s" % str(ping)
                title = "Probe not avaible"
                data = urllib.urlencode({'pushtext': str(message),'title': title})
                req = urllib2.Request(urlForNotification,data)
                urllib2.urlopen(req)
                ip_device_list_Error.append(ping)
        else:
            address = "192.168.0." + str(ping)
            res = subprocess.call(['ping', '-c', '1', address])
            if res == 0:
                print "ping to", address, "OK "
                message = "Probe %s is now working yet" % str(ping)
                title = "Probe Finded"
                data = urllib.urlencode({'pushtext': str(message),'title': title})
                req = urllib2.Request(urlForNotification,data)
                urllib2.urlopen(req)
                ip_device_list_Error.remove(ping)
            else:
                print "ping to", address, "failed!"
    time.sleep(60)
