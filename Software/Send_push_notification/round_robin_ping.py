#to use this push notification, you need to buy Pushover on Android Play or Apple Store

import httplib, urllib
import subprocess

list_ip_to_check = ["211","202","111"]

for ping in list_ip_to_check:
    address = "192.168.0." + str(ping)
    res = subprocess.call(['ping', '-c', '1', address])
    if res == 0:
        print "ping to", address, "OK "
    elif res == 2:
        print "no response from", address
        conn = httplib.HTTPSConnection("api.pushover.net:443")
		conn.request("POST", "/1/messages.json",
		urllib.urlencode({
		"token": "INSERT-TOKEN-HERE",
		"user": "INSERT-USER-HERE",
		"message": "ping to ", address, "fail ",
		}), { "Content-type": "application/x-www-form-urlencoded" })
		conn.getresponse()
    else:
        print "ping to", address, "failed!"
        conn = httplib.HTTPSConnection("api.pushover.net:443")
		conn.request("POST", "/1/messages.json",
		urllib.urlencode({
		"token": "INSERT-TOKEN-HERE",
		"user": "INSERT-USER-HERE",
		"message": "ping to ", address, "fail ",
		}), { "Content-type": "application/x-www-form-urlencoded" })
		conn.getresponse()
