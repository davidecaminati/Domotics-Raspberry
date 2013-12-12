import RPIO.PWM as PWM
import time
from flask import Flask, url_for, request

#variable
hostIP = '192.168.0.100'
app = Flask(__name__)
app.config.from_object(__name__)

GPIO_RED = 17
GPIO_GREEN = 27
GPIO_BLUE = 22
r = 0
g = 0
b = 0

CHANNEL = 0

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
        red = request.form['r']
        green = request.form['g']
        blue = request.form['b']
 
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
@app.route('/colorchange2/<string:red>/<string:green>/<string:blue>', methods=['GET', 'POST'])
def api_colorchange2(red,green,blue):
#PWM.print_channel(CHANNEL)
    
    PWM.add_channel_pulse(CHANNEL, GPIO_RED, 0, int(red))
    PWM.add_channel_pulse(CHANNEL, GPIO_GREEN, 0, int(green))
    PWM.add_channel_pulse(CHANNEL, GPIO_BLUE, 0, int(blue))
    return 'ok'
        
if __name__ == '__main__':
    app.debug=True
    app.run(host=hostIP)