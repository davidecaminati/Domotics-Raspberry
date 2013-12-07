from flask import Flask, url_for
import smbus
import time

#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1
DEVICE = 0x20 # Device address (A0-A2)
IODIRA = 0x00 # Pin direction register
OLATA  = 0x14 # Register for outputs
GPIOA  = 0x12 # Register for inputs

# Set all GPA pins as outputs by setting
# all bits of IODIRA register to 0
bus.write_byte_data(DEVICE,IODIRA,0x00)

#variable
hostIP = '192.168.0.100'
app = Flask(__name__)

blue = 1
green = 2
cyan = 3
red = 4
violet = 5
yellow = 6
white = 7


bus.write_byte_data(DEVICE,OLATA,0)

#app.debug = True
@app.route('/')
def api_root():
    return 'Welcome on %s' % hostIP

@app.route('/color/<string:colore>', methods=['POST','GET'])
def api_color(colore):
    # Set output all 7 output bits to 0
    bus.write_byte_data(DEVICE,OLATA,0)  
    if colore == "red":
        bus.write_byte_data(DEVICE,OLATA,red)
    elif colore == "green":
           bus.write_byte_data(DEVICE,OLATA,green)
    elif colore == "blue":
           bus.write_byte_data(DEVICE,OLATA,blue)
    elif colore == "cyan":
           bus.write_byte_data(DEVICE,OLATA,cyan)
    elif colore == "violet":
           bus.write_byte_data(DEVICE,OLATA,violet)
    elif colore == "yellow":
           bus.write_byte_data(DEVICE,OLATA,yellow)
    elif colore == "white":
           bus.write_byte_data(DEVICE,OLATA,white)
    else:
        bus.write_byte_data(DEVICE,OLATA,0)
        return "error"
    return 'ok'


if __name__ == '__main__':
    app.run(host=hostIP)
