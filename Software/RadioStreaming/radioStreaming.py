#!/usr/bin/python
import urllib
import urllib2
import pygame
import subprocess
import redis
import time
import os
from random import randint
from flask import Flask, url_for #, render_template, request, jsonify

server_redis = '127.0.0.1'

app = Flask(__name__)

@app.route('/')
def api_root():
    documentation = ('Welcome <br>'
    'this is the list of API implemented: <br>'
    '<br>'
    '/play/[number] <br>'
    'play [number].mp3 in the folder home/pi/mp3/ <br>'
    '<br>'
    '/stop <br>'
    'stop all songs  <br>'
    '<br>'
    '/shutdown <br>'
    'shutdown this computer <br>'
    '<br>'
    '/reboot <br>'
    'reboot this computer <br>'
    '<br>'
    '/setredis/[campo]/[valore]  <br>'
    'save value in the database redis  <br>'
    '<br>'
    '/getredis/[campo] <br>'
    'get value from the database redis in the field specified <br>'
    '<br>'
    '/getredis/[campo]/[validita] <br>'
    'get value from the database redis in the field specified only if the value are saved less the [validita] seconds <br>'
    'otherwise return -- <br>'
    '<br>'
    '/getinfo/[campo] <br>'
    'get info about the state of computer (ex "tempcpu" for cpu temperature,"cpuuse" for cpu used, "ramfree" for free ram im KB) <br>'
    '/ <br>'
    'this help <br>'
    )
    return documentation

@app.route('/play/<int:number>')
def api_play(number):
    print number
    file = str(number) + '.mp3'
    print file
    p = subprocess.Popen(['mpg123', '/home/pi/mp3/' + file])
    return "play", 201, {'Access-Control-Allow-Origin': '*'} 
    
@app.route('/stop')
def api_stop():
    k = subprocess.Popen(['killall', 'mpg123'])
    return "stop" , 201, {'Access-Control-Allow-Origin': '*'} 
    
@app.route('/getinfo/<campo>')
def api_getinfo(campo):
#thanks to PhJulien posted into http://www.raspberrypi.org/forums/viewtopic.php?f=32&t=22180
    valore = ""
    if str(campo) == "tempcpu":
        valore = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
    if str(campo) == "cpuuse":
        valore = str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip())
    if str(campo) == "ramfree":
        p = os.popen('free')
        i = 0
        while i < 3:
            i = i + 1
            line = p.readline()
            if i==2:
                valore = line.split()[1:4][2]
    return str(valore) , 201, {'Access-Control-Allow-Origin': '*'} 
    
@app.route('/shutdown')
def api_shutdown():
    #k = subprocess.Popen(['sudo','shutdown'])
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    return "shutdown" , 201, {'Access-Control-Allow-Origin': '*'} 
    
@app.route('/reboot')
def api_reboot():
    k = subprocess.Popen(['sudo','reboot'])
    return "reboot" , 201, {'Access-Control-Allow-Origin': '*'} 
    
@app.route('/setredis/<campo>/<valore>')
def api_setredis(campo,valore):
    pool = redis.ConnectionPool(host=server_redis, port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    ts = time.time()
    r.rpush(campo,str(valore))
    r.rpush(campo + "timestamp",int(ts))
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

def get_elapsed_time(campo):
    pool = redis.ConnectionPool(host=server_redis, port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    field_timestamps = r.lrange(campo + "timestamp",'-1','-1')
    if len(field_timestamps) >= 1:
        field_timestamp = int(field_timestamps[0])
    else :
        field_timestamp = 0
    ts = int(time.time())
    elapsed = ts - field_timestamp
    return elapsed
    
@app.route('/getredis/<campo>/<validita>')
def api_getredisvalidita(campo,validita):
    pool = redis.ConnectionPool(host=server_redis, port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    valori = r.lrange(campo,'-1','-1')
    valore = ""
    elapsed = get_elapsed_time(campo)
    print elapsed
    print int(validita)
    if elapsed <= int(validita):
        if len(valori) >= 1:
            valore = valori[0]
        else:
            valore = "errore"
    else:
        valore = "--"
    return str(valore) , 201, {'Access-Control-Allow-Origin': '*'} 
    
if __name__ == '__main__':
    app.run(host='192.168.0.208',debug = True)