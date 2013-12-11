import RPIO.PWM as PWM
import time
from flask import Flask, url_for

#variable
hostIP = '192.168.0.100'
app = Flask(__name__)
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
@app.route('/colorchange/<int:r>/<int:g>/<int:b>', methods=['POST','GET'])
def api_colorchange(r,g,b):
#PWM.print_channel(CHANNEL)
    PWM.add_channel_pulse(CHANNEL, GPIO_RED, 0, r)
    PWM.add_channel_pulse(CHANNEL, GPIO_GREEN, 0, g)
    PWM.add_channel_pulse(CHANNEL, GPIO_BLUE, 0, b)
    #time.sleep(0.01)
    return 'r:%s g:%s b:%s' % (r,g,b)
#PWM.add_channel_pulse(CHANNEL, GPIO_BLUE, 100, 50)

#time.sleep(5)
# Stop PWM for specific GPIO on channel 0
#PWM.clear_channel_gpio(0, GPIO_BLUE)

#PWM.cleanup()
if __name__ == '__main__':
    app.run(host=hostIP)