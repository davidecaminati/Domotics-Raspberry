import urllib
import urllib2
import pygame
import subprocess
from random import randint
from flask import Flask, url_for #, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/play/<int:number>')
def api_play(number):
    print number
    file = str(number) + '.mp3'
    print file
    #file = 'http://kos.broadstreamer.com:8500'
    #pygame.init()
    #pygame.mixer.init()
    #pygame.mixer.music.load(file)
    #pygame.mixer.music.play()
    
    #from subprocess import call
    #call(["killall", "mpg123"])
    #call(["mpg123", file])
    #api_stop()
    p = subprocess.Popen(['mpg123', '/home/pi/Domotics-Raspberry/Software/RadioStreaming/' + file])
    return "play"
    
@app.route('/stop')
def api_stop():
    k = subprocess.Popen(['killall', 'mpg123'])
    return "stop"
    
    
if __name__ == '__main__':
    app.run(host='192.168.0.110',debug = True)