import httplib, urllib
import subprocess

lista_ip_dispositivi = ["211","202","111"]

for ping in lista_ip_dispositivi:
    address = "192.168.0." + str(ping)
    res = subprocess.call(['ping', '-c', '1', address])
    if res == 0:
        print "ping to", address, "OK "
    elif res == 2:
        print "no response from", address
        conn = httplib.HTTPSConnection("api.pushover.net:443")
		conn.request("POST", "/1/messages.json",
		urllib.urlencode({
		"token": "abdf67yAvRcQufveo2nGkwKNi6xTHb",
		"user": "u2v1vYFWvmGGNGN3Ffnn9NnCW1Y3xN",
		"message": "hello world",
		}), { "Content-type": "application/x-www-form-urlencoded" })
		conn.getresponse()
    else:
        print "ping to", address, "failed!"
        conn = httplib.HTTPSConnection("api.pushover.net:443")
		conn.request("POST", "/1/messages.json",
		urllib.urlencode({
		"token": "abdf67yAvRcQufveo2nGkwKNi6xTHb",
		"user": "u2v1vYFWvmGGNGN3Ffnn9NnCW1Y3xN",
		"message": "hello world",
		}), { "Content-type": "application/x-www-form-urlencoded" })
		conn.getresponse()





