import urllib
import urllib2
import pygame
import subprocess
import redis
import time
from random import randint
from flask import Flask, url_for #, render_template, request, jsonify


server_redis = '127.0.0.1'

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
    return "stop" , 201, {'Access-Control-Allow-Origin': '*'} 
    
    
@app.route('/setredis/<campo>/<valore>')
def api_setredis(campo,valore):
    pool = redis.ConnectionPool(host=server_redis, port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    ts = time.time()
    r.rpush(campo,str(valore))
    r.rpush(campo + "timestamp",str(ts))
    return "ok", 201, {'Access-Control-Allow-Origin': '*'} 
    
@app.route('/getredis/<campo>')
def api_getredis(campo):
    pool = redis.ConnectionPool(host=server_redis, port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    valori = r.lrange(campo,'-1','-1')
    valore = ""
    if len(valori) >= 1:
        valore = valori[0]
    else:
        valore = "errore"
    return valore , 201, {'Access-Control-Allow-Origin': '*'} 
    
    
if __name__ == '__main__':
    app.run(host='192.168.0.208',debug = True)