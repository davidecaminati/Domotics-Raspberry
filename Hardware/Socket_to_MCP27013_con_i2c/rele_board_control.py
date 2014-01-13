
import smbus
import time
import urllib
import urllib2
from flask import Flask, url_for
# IODIRA   0x00   // IO direction  (0 = output, 1 = input (Default))
# IODIRB   0x01
# IOPOLA   0x02   // IO polarity   (0 = normal, 1 = inverse)
# IOPOLB   0x03
# GPINTENA 0x04   // Interrupt on change (0 = disable, 1 = enable)
# GPINTENB 0x05
# DEFVALA  0x06   // Default comparison for interrupt on change (interrupts on opposite)
# DEFVALB  0x07
# INTCONA  0x08   // Interrupt control (0 = interrupt on change from previous, 1 = interrupt on change from DEFVAL)
# INTCONB  0x09
# IOCON    0x0A   // IO Configuration: bank/mirror/seqop/disslw/haen/odr/intpol/notimp
# IOCON 0x0B  // same as 0x0A
# GPPUA    0x0C   // Pull-up resistor (0 = disabled, 1 = enabled)
# GPPUB    0x0D
# INFTFA   0x0E   // Interrupt flag (read only) : (0 = no interrupt, 1 = pin caused interrupt)
# INFTFB   0x0F
# INTCAPA  0x10   // Interrupt capture (read only) : value of GPIO at time of last interrupt
# INTCAPB  0x11
# GPIOA    0x12   // Port value. Write to change, read to obtain value
# GPIOB    0x13
# OLLATA   0x14   // Output latch. Write to latch output.
# OLLATB   0x15

bus20 = smbus.SMBus(1) # Rev 2 Pi uses 1

DEVICE20 = 0x20 # DEVICE2020 address (A0-A2)
IODIRA = 0x00 # Pin direction register for port A
IODIRB = 0x01 # Pin direction register for port B
OLATA  = 0x14 # Register for outputs for port A
OLATB  = 0x15 # Register for outputs for port B
GPIOA  = 0x12 # Register for inputs for port A
GPIOB  = 0x13 # Register for inputs for port B
GPPUA  = 0x0C # Pull-up resistor (0 = disabled, 1 = enabled)
GPPUB  = 0x0D # Pull-up resistor (0 = disabled, 1 = enabled)

bus20.write_byte_data(DEVICE20,IODIRA,0x00)

# Set PullUp resistor for input register
#bus20.write_byte_data(DEVICE20,GPPUA,0x00) #11111111
bus20.write_byte_data(DEVICE20,GPPUB,0xff) #11111111

app = Flask(__name__)
#while True:
#    print bus20.read_byte_data(DEVICE20,GPIOB)

@app.route('/')
def api_root():
    return 'Welcome'


@app.route('/releoff/<int:number>')
def api_releoff(number):
    if number > 8 or number < 1:
        print 'this rele not exist \n'
        return 'error'
    NeedChange = False
    OldState = bus20.read_byte_data(DEVICE20,GPIOB)
    BinReleNumber = 2** (number - 1)
    if OldState == 0:
        NeedChange = True
        bus20.write_byte_data(DEVICE20,OLATA,BinReleNumber)
    else:
        #is already on ?
        print 'number ' + str(number) + '\n'
        print 'OldState ' + str(OldState) + '\n'
        print 'BinReleNumber ' + str(BinReleNumber) + '\n'
        if BinReleNumber & OldState == BinReleNumber:
            NeedChange = False
            print 'already done \n'
            return 'already done'
        else:
            NeedChange = True
            bus20.write_byte_data(DEVICE20,OLATA,BinReleNumber)
    time.sleep(0.3)
    bus20.write_byte_data(DEVICE20,OLATA,0)
    time.sleep(0.3)
    #test if rele has changed
    NewState = bus20.read_byte_data(DEVICE20,GPIOB)
    print NewState
    print OldState
    if NeedChange:
        if NewState != OldState:
            return 'ok'
        else:
            return 'malfunction'

@app.route('/releon/<int:number>')
def api_releon(number):
    if number > 8 or number < 1:
        print 'this rele not exist \n'
        return 'error'
    NeedChange = False
    OldState = bus20.read_byte_data(DEVICE20,GPIOB)
    BinReleNumber = 2** (number - 1)
    if OldState == 255:
        #print 'OldState == 255'
        NeedChange = True
        bus20.write_byte_data(DEVICE20,OLATA,BinReleNumber)
    else:
        #is already off ?
        print 'number ' + str(number) + '\n'
        print 'OldState ' + str(OldState) + '\n'
        print 'BinReleNumber ' + str(BinReleNumber) + '\n'
        #print '(255 - BinReleNumber) ' + str(255 - BinReleNumber) + '\n'
        # print 'OldState == 255 - BinReleNumber ' + OldState == 255 - BinReleNumber + '\n'

        if BinReleNumber & OldState != BinReleNumber:
            NeedChange = False
            print 'already done \n'
            return 'already done'
        else:
            print 'NeedChange'
            NeedChange = True
            bus20.write_byte_data(DEVICE20,OLATA,BinReleNumber)
    time.sleep(0.3)
    bus20.write_byte_data(DEVICE20,OLATA,0)
    time.sleep(0.3)
    #test if rele has changed
    NewState = bus20.read_byte_data(DEVICE20,GPIOB)
    print NewState
    print OldState
    if NeedChange:
        if NewState != OldState:
            return 'ok'
        else:
            return 'malfunction'

@app.route('/reletoggle/<int:number>')
def api_reletoggle(number):
    if number > 8 or number < 1:
        print 'this rele not exist \n'
        return 'error'
    NeedChange = False
    OldState = bus20.read_byte_data(DEVICE20,GPIOB)
    BinReleNumber = 2** (number - 1)
    print 'number ' + str(number) + '\n'
    print 'OldState ' + str(OldState) + '\n'
    print 'BinReleNumber ' + str(BinReleNumber) + '\n'
    print 'toggle'
    bus20.write_byte_data(DEVICE20,OLATA,BinReleNumber)
    time.sleep(0.1)
    bus20.write_byte_data(DEVICE20,OLATA,0)
    time.sleep(0.1)
    #test if rele has changed
    NewState = bus20.read_byte_data(DEVICE20,GPIOB)
    print NewState
    print OldState
    if OldState != NewState:
        return 'ok'
    else:
        return "malfunction"
    
@app.route('/reledimmon/<int:number>')
def api_reledimmon(number):
    if number > 8 or number < 1:
        print 'this rele not exist \n'
        return 'error'
    BinReleNumber = 2** (number - 1)
    print "BinReleNumber",BinReleNumber
    bus20.write_byte_data(DEVICE20,OLATA,BinReleNumber)
    return 'ok'

@app.route('/reledimmoff/<int:number>')
def api_reledimmoff(number):
    if number > 8 or number < 1:
        print 'this rele not exist \n'
        return 'error'
    bus20.write_byte_data(DEVICE20,OLATA,0)
    lastStateDimm = 0
    return 'ok'

@app.route('/reletimer/<int:number>/<int:unlock_after_millisec>')
def api_reletimer(number,unlock_after_millisec):
    milliseconds = 0.0
    milliseconds = float(unlock_after_millisec) / 1000.0
    if number > 8 or number < 1:
        print 'this rele not exist \n'
        return 'error'
    BinReleNumber = 2** (number - 1)
    bus20.write_byte_data(DEVICE20,OLATA,BinReleNumber)
    time.sleep(milliseconds)
    bus20.write_byte_data(DEVICE20,OLATA,0)
    return "ok" 

@app.route('/relestate/<int:number>')
def api_relestate(number):
    if number > 8 or number < 1:
        print 'this rele not exist \n'
        return 'error'
    OldState = bus20.read_byte_data(DEVICE20,GPIOB)
    BinReleNumber = 2** (number - 1)
    #is already on ?
    if BinReleNumber & OldState == BinReleNumber:
        return 'off'
    else:
        return 'on'

@app.route('/relestateall/')
def api_relestateall():
    State = bus20.read_byte_data(DEVICE20,GPIOB)
    #BinReleNumber = bin(OldState)
    print State
    #print BinReleNumber
    return str(State)
    


if __name__ == '__main__':
    app.run(host='192.168.0.202')
    
