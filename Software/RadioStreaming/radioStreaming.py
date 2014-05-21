import urllib
import urllib2
from random import randint
from flask import Flask, url_for #, render_template, request, jsonify


app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/play/<int:number>')
def api_facedetected(number):
            file = str(number) + '.mp3'
            #file = 'http://kos.broadstreamer.com:8500'
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
    return "ok"
    
    
if __name__ == '__main__':
    app.run(host='192.168.0.208',debug = True)