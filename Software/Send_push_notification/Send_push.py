from flask import Flask, url_for

#variable
hostIP = '192.168.0.208'
app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Welcome on %s' % hostIP
	

@app.route('/send_push/<string:pushtext>')
def api_send_push(pushtext):
    conn = httplib.HTTPSConnection("api.pushover.net:443")
	conn.request("POST", "/1/messages.json",urllib.urlencode({"token": "abdf67yAvRcQufveo2nGkwKNi6xTHb","user": "u2v1vYFWvmGGNGN3Ffnn9NnCW1Y3xN","message": pushtext,"title": "Notification"}), { "Content-type": "application/x-www-form-urlencoded" })
	conn.getresponse()
	return 'ok'


if __name__ == '__main__':
    app.run(host=hostIP)