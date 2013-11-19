import httplib, urllib
import subprocess

device_ip_list = ["211","202"]

for ping in device_ip_list:
    address = "192.168.0." + str(ping)
    res = subprocess.call(['ping', '-c', '1', address])
    if res == 0:
        print "ping to", address, "OK "
    elif res == 2:
        print "no response from ", address
        conn = httplib.HTTPSConnection("api.pushover.net:443")
		conn.request("POST", "/1/messages.json",
		urllib.urlencode({
		"token": "INSERT-TOKEN-HERE",
		"user": "INSERT-USER-HERE",
		"message": "no response from %s" % address,
		}), { "Content-type": "application/x-www-form-urlencoded" })
		conn.getresponse()
    else:
        print "ping to", address, "failed!"
        conn = httplib.HTTPSConnection("api.pushover.net:443")
		conn.request("POST", "/1/messages.json",
		urllib.urlencode({
		"token": "INSERT-TOKEN-HERE",
		"user": "INSERT-USER-HERE",
		"message": "no response from %s" % address,
		}), { "Content-type": "application/x-www-form-urlencoded" })
		conn.getresponse()





