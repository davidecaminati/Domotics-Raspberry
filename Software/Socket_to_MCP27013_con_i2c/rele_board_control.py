from flask import Flask, url_for
import smbus
import time

bus = smbus.SMBus(1) # Rev 2 Pi uses 1
DEVICE = 0x20 # Device address (A0-A2)
IODIRA = 0x00 # Pin direction register
OLATA  = 0x14 # Register for outputs
GPIOA  = 0x12 # Register for output
GPIOB  = 0x13 # Register for inputs
hostIP = '192.168.0.202'

bus.write_byte_data(DEVICE,IODIRA,0x00)
app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/releon/<int:number>')
def api_releon(number):
    if number > 8 or number < 1:
        print 'this rele not exist \n'
        return 'error'
    NeedChange = False
    OldState = bus.read_byte_data(DEVICE,GPIOB)
    BinReleNumber = 2** (number - 1)
    if OldState == 0:
        NeedChange = True
        bus.write_byte_data(DEVICE,OLATA,BinReleNumber)
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
            bus.write_byte_data(DEVICE,OLATA,BinReleNumber)
    time.sleep(0.3)
    bus.write_byte_data(DEVICE,OLATA,0)
    time.sleep(0.3)
    #test if rele has changed
    NewState = bus.read_byte_data(DEVICE,GPIOB)
    print NewState
    print OldState
    if NeedChange:
        if NewState != OldState:
            return 'ok'
        else:
            return 'malfunction'

@app.route('/releoff/<int:number>')
def api_releoff(number):
    if number > 8 or number < 1:
        print 'this rele not exist \n'
        return 'error'
    NeedChange = False
    OldState = bus.read_byte_data(DEVICE,GPIOB)
    BinReleNumber = 2** (number - 1)
    if OldState == 255:
        #print 'OldState == 255'
        NeedChange = True
        bus.write_byte_data(DEVICE,OLATA,BinReleNumber)
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
            bus.write_byte_data(DEVICE,OLATA,BinReleNumber)
    time.sleep(0.3)
    bus.write_byte_data(DEVICE,OLATA,0)
    time.sleep(0.3)
    #test if rele has changed
    NewState = bus.read_byte_data(DEVICE,GPIOB)
    print NewState
    print OldState
    if NeedChange:
        if NewState != OldState:
            return 'ok'
        else:
            return 'malfunction'

if __name__ == '__main__':
    app.run(host=hostIP)
