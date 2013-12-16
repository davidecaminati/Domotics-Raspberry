import RPIO.PWM as PWM
import time
from flask import Flask, url_for, request
import commands
#variable
app = Flask(__name__)
app.config.from_object(__name__)

GPIO_RED = 17
GPIO_GREEN = 27
GPIO_BLUE = 22
Correction_RED = 0.6
Correction_GREEN = 1.0
Correction_BLUE = 0.4
Correction_RED1 = 1.0
Correction_GREEN1 = 1.0
Correction_BLUE1 = 1.0

r = 0.0
g = 0.0
b = 0.0

CHANNEL = 0
# get ip
#intf = 'eth0'
#intf_ip = commands.getoutput("ip address show dev " + intf).split()
#intf_ip = intf_ip[intf_ip.index('inet') + 1].split('/')[0]
#hostIP =  intf_ip
# or set ip
hostIP = '192.168.0.100'

PWM.setup()
PWM.init_channel(CHANNEL,4000)
#app.debug = True
@app.route('/')
def api_root():
    return 'Welcome on %s' % hostIP

#PWM.set_loglevel(PWM.LOG_LEVEL_DEBUG)
@app.route('/colorchange', methods=['GET', 'POST'])
def api_colorchange():
#PWM.print_channel(CHANNEL)
    if request.method == 'POST':
        red_raw = request.form['r']
        red = int(red_raw) * Correction_RED1
        print "red %s" % red
        green_raw = request.form['g']
        green = int(green_raw) * Correction_GREEN1
        print "green %s" % green
        blue_raw = request.form['b']
        blue = int(blue_raw) * Correction_BLUE1 
        print "blue %s" %blue
        PWM.add_channel_pulse(CHANNEL, GPIO_RED, 0, int(red))
        PWM.add_channel_pulse(CHANNEL, GPIO_GREEN, 0, int(green))
        PWM.add_channel_pulse(CHANNEL, GPIO_BLUE, 0, int(blue))
        return 'post %s' % r
    else:
        return 'get'
    #red = session.get('r')
    #green = session.get('g')
    #blue = session.get('b')
    #PWM.add_channel_pulse(CHANNEL, GPIO_RED, 0, int(red))
    #PWM.add_channel_pulse(CHANNEL, GPIO_GREEN, 0, int(green))
    #PWM.add_channel_pulse(CHANNEL, GPIO_BLUE, 0, int(blue))
    #time.sleep(0.01)
    #return x
#PWM.add_channel_pulse(CHANNEL, GPIO_BLUE, 100, 50)

#time.sleep(5)
# Stop PWM for specific GPIO on channel 0
#PWM.clear_channel_gpio(0, GPIO_BLUE)

#PWM.cleanup()
@app.route('/colorchange2/<string:red_raw>/<string:green_raw>/<string:blue_raw>', methods=['GET', 'POST'])
def api_colorchange2(red_raw,green_raw,blue_raw):
#PWM.print_channel(CHANNEL)
    
    red = int(red_raw) * Correction_RED
    print "red %s" % red
    green = int(green_raw) * Correction_GREEN
    print "green %s" % green
    blue = int(blue_raw) * Correction_BLUE
    print "blue %s" %blue
        
    PWM.add_channel_pulse(CHANNEL, GPIO_RED, 10, int(red))
    PWM.add_channel_pulse(CHANNEL, GPIO_GREEN, 0, int(green))
    PWM.add_channel_pulse(CHANNEL, GPIO_BLUE, 0, int(blue))
    return 'ok'
        
if __name__ == '__main__':
    app.debug=True
    app.run(host=hostIP)