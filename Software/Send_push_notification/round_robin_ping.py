import httplib, urllib 
import subprocess 
import time
#205 digital probe
#208 monitor TFT  server web
#86 PC windows
#202 rele
#211 analog Probe
ip_device_list = [9,211,208] 
ip_device_list_Error = []
for ping in ip_device_list:
	print ip_device_list
	print ip_device_list_Error
	
	if (ping in ip_device_list_Error) == False:
		address = "192.168.0." + str(ping)
		res = subprocess.call(['ping', '-c', '1', address])
		if res == 0:
			print "ping to", address, "OK "
			#conn = httplib.HTTPSConnection("api.pushover.net:443")
			#conn.request("POST", "/1/messages.json",urllib.urlencode({"token": "abdf67yAvRcQufveo2nGkwKNi6xTHb","user": "u2v1vYFWvmGGNGN3Ffnn9NnCW1Y3xN","message": "hello world",}), { "Content-type": "application/x-www-form-urlencoded" })
			#conn.getresponse()
		elif res == 2:
			print "no response from", address
			conn = httplib.HTTPSConnection("api.pushover.net:443")
			conn.request("POST", "/1/messages.json",urllib.urlencode({"token": "abdf67yAvRcQufveo2nGkwKNi6xTHb","user": "u2v1vYFWvmGGNGN3Ffnn9NnCW1Y3xN","message": "error from  %s" % address,"title": "Probe not avaible"}), { "Content-type": "application/x-www-form-urlencoded" })
			conn.getresponse()
			ip_device_list_Error.append(ping)
		else:
			print "ping to", address, "failed!"
			conn = httplib.HTTPSConnection("api.pushover.net:443")
			conn.request("POST", "/1/messages.json",urllib.urlencode({"token": "abdf67yAvRcQufveo2nGkwKNi6xTHb","user": "u2v1vYFWvmGGNGN3Ffnn9NnCW1Y3xN","message": "error from  %s" % address,"title": "Probe not avaible"}), { "Content-type": "application/x-www-form-urlencoded" })
			conn.getresponse()
			ip_device_list_Error.append(ping)
	else:
		address = "192.168.0." + str(ping)
		res = subprocess.call(['ping', '-c', '1', address])
		if res == 0:
			print "ping to", address, "OK "
			conn = httplib.HTTPSConnection("api.pushover.net:443")
			conn.request("POST", "/1/messages.json",urllib.urlencode({"token": "abdf67yAvRcQufveo2nGkwKNi6xTHb","user": "u2v1vYFWvmGGNGN3Ffnn9NnCW1Y3xN","message": "Probe %s is now working yet" % address,"title": "Probe Finded"}), { "Content-type": "application/x-www-form-urlencoded" })
			conn.getresponse()
			ip_device_list_Error.remove(ping)
		elif res == 2:
			print "no response from", address
			#conn = httplib.HTTPSConnection("api.pushover.net:443")
			#conn.request("POST", "/1/messages.json",urllib.urlencode({"token": "abdf67yAvRcQufveo2nGkwKNi6xTHb","user": "u2v1vYFWvmGGNGN3Ffnn9NnCW1Y3xN","message": "error from  %s" % address,"title": "Probe not avaible"}), { "Content-ty$
			#conn.getresponse()
		else:
			print "ping to", address, "failed!"
			#conn = httplib.HTTPSConnection("api.pushover.net:443")
			#conn.request("POST", "/1/messages.json",urllib.urlencode({"token": "abdf67yAvRcQufveo2nGkwKNi6xTHb","user": "u2v1vYFWvmGGNGN3Ffnn9NnCW1Y3xN","message": "error from  %s" % address,"title": "Probe not avaible"}), { "Content-ty$
			#conn.getresponse()

#time.sleep(60)
