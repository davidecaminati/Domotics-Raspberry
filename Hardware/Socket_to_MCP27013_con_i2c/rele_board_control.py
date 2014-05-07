
import smbus
import time
import urllib
import urllib2
import redis
from flask import Flask, url_for #, render_template, request, jsonify
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
#    #print bus20.read_byte_data(DEVICE20,GPIOB)

server_redis = '192.168.0.208'

@app.route('/facedetected/<int:number>/<string:name>')
def api_facedetected(number,name):
    ts = time.time()
    pool = redis.ConnectionPool(host=server_redis, port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    r.rpush("facedetectedtimestamp",str(ts))
    r.rpush("facedetectedQuality",str(number))
    r.rpush("facedetectedName",str(name))
    return "ok"
    
def GetReleState():
    return 255-bus20.read_byte_data(DEVICE20,GPIOB)

@app.route('/')
def api_root():
    return 'Welcome'


@app.route('/releoff/<int:number>')
def api_releoff(number):
    if number > 8 or number < 1:
        #print 'this rele not exist \n'
        return 'error', 201, {'Access-Control-Allow-Origin': '*'} 
    NeedChange = False
    OldState = bus20.read_byte_data(DEVICE20,GPIOB)
    BinReleNumber = 2** (number - 1)
    if OldState == 0:
        NeedChange = True
        bus20.write_byte_data(DEVICE20,OLATA,BinReleNumber)
    else:
        #is already on ?
        #print 'number ' + str(number) + '\n'
        #print 'OldState ' + str(OldState) + '\n'
        #print 'BinReleNumber ' + str(BinReleNumber) + '\n'
        if BinReleNumber & OldState == BinReleNumber:
            NeedChange = False
            #print 'already done \n'
            return 'already done', 201, {'Access-Control-Allow-Origin': '*'} 
        else:
            NeedChange = True
            bus20.write_byte_data(DEVICE20,OLATA,BinReleNumber)
    time.sleep(0.3)
    bus20.write_byte_data(DEVICE20,OLATA,0)
    time.sleep(0.3)
    #test if rele has changed
    NewState = bus20.read_byte_data(DEVICE20,GPIOB)
    #print NewState
    #print OldState
    if NeedChange:
        if NewState != OldState:
            return 'ok', 201, {'Access-Control-Allow-Origin': '*'} 
        else:
            return 'malfunction', 201, {'Access-Control-Allow-Origin': '*'} 

@app.route('/releon/<int:number>')
def api_releon(number):
    if number > 8 or number < 1:
        #print 'this rele not exist \n'
        return 'error', 201, {'Access-Control-Allow-Origin': '*'} 
    NeedChange = False
    OldState = bus20.read_byte_data(DEVICE20,GPIOB)
    BinReleNumber = 2** (number - 1)
    if OldState == 255:
        ##print 'OldState == 255'
        NeedChange = True
        bus20.write_byte_data(DEVICE20,OLATA,BinReleNumber)
    else:
        #is already off ?
        #print 'number ' + str(number) + '\n'
        #print 'OldState ' + str(OldState) + '\n'
        #print 'BinReleNumber ' + str(BinReleNumber) + '\n'
        ##print '(255 - BinReleNumber) ' + str(255 - BinReleNumber) + '\n'
        # #print 'OldState == 255 - BinReleNumber ' + OldState == 255 - BinReleNumber + '\n'

        if BinReleNumber & OldState != BinReleNumber:
            NeedChange = False
            #print 'already done \n'
            return 'already done', 201, {'Access-Control-Allow-Origin': '*'} 
        else:
            #print 'NeedChange'
            NeedChange = True
            bus20.write_byte_data(DEVICE20,OLATA,BinReleNumber)
    time.sleep(0.3)
    bus20.write_byte_data(DEVICE20,OLATA,0)
    time.sleep(0.3)
    #test if rele has changed
    NewState = bus20.read_byte_data(DEVICE20,GPIOB)
    #print NewState
    #print OldState
    if NeedChange:
        if NewState != OldState:
            return 'ok', 201, {'Access-Control-Allow-Origin': '*'} 
            
        else:
            return 'malfunction' , 201, {'Access-Control-Allow-Origin': '*'} 
            
        
@app.route('/reletest')
def api_reletest():
    #return jsonify(result='2'), 201, {'Access-Control-Allow-Origin': '*'} 
    return "ok", 201, {'Access-Control-Allow-Origin': '*'} 
    
      
def ReleNumberExist(numbers):
    r = range(1,9)
    for n in numbers:
        if not n in r:
            return False
    return True

@app.route('/multireleon/<int:number1>/<int:number2>/<int:number3>/<int:number4>/<int:number5>')
def api_multireleon(number1,number2,number3,number4,number5):
    if not ReleNumberExist([number1,number2,number3,number4,number5]):
        #print 'one of this rele not exist \n'
        return 'error', 201, {'Access-Control-Allow-Origin': '*'} 
    NeedChange = False
    OldState = bus20.read_byte_data(DEVICE20,GPIOB)
    BinReleNumber1 = 2** (number1 - 1)
    BinReleNumber2 = 2** (number2 - 1)
    BinReleNumber3 = 2** (number3 - 1)
    BinReleNumber4 = 2** (number4 - 1)
    BinReleNumber5 = 2** (number5 - 1)
    BinReleNumber =  (BinReleNumber1 | BinReleNumber2 | BinReleNumber3 | BinReleNumber4 | BinReleNumber5 )

    #print 'OldState ' , OldState
    #print 'BinReleNumber ' , BinReleNumber
    toChange = OldState &  BinReleNumber
    #print "toChange" , toChange
    if OldState == 255: # all off
        NeedChange = True
        bus20.write_byte_data(DEVICE20,OLATA,toChange)
    else:
        if toChange == 0:
            NeedChange = False
            #print 'already done \n'
            return 'already done', 201, {'Access-Control-Allow-Origin': '*'} 
        else:
            #print 'NeedChange'
            NeedChange = True
            bus20.write_byte_data(DEVICE20,OLATA,toChange)
            
    time.sleep(0.3)
    bus20.write_byte_data(DEVICE20,OLATA,0)
    time.sleep(0.3)
    NewState = bus20.read_byte_data(DEVICE20,GPIOB)
    #print NewState
    #print OldState
    if NeedChange:
        if NewState != OldState:
            return 'ok', 201, {'Access-Control-Allow-Origin': '*'} 
        else:
            return 'malfunction', 201, {'Access-Control-Allow-Origin': '*'} 
        
@app.route('/multireleoff/<int:number1>/<int:number2>/<int:number3>/<int:number4>/<int:number5>')
def api_multireleoff(number1,number2,number3,number4,number5):
    if not ReleNumberExist([number1,number2,number3,number4,number5]):
        #print 'one of this rele not exist \n'
        return 'error', 201, {'Access-Control-Allow-Origin': '*'} 
    NeedChange = False
    OldState = bus20.read_byte_data(DEVICE20,GPIOB)
    BinReleNumber1 = 2** (number1 - 1)
    BinReleNumber2 = 2** (number2 - 1)
    BinReleNumber3 = 2** (number3 - 1)
    BinReleNumber4 = 2** (number4 - 1)
    BinReleNumber5 = 2** (number5 - 1)
    BinReleNumber =  (BinReleNumber1 | BinReleNumber2 | BinReleNumber3 | BinReleNumber4 | BinReleNumber5 )

    #print 'OldState ' , OldState
    #print 'BinReleNumber ' , BinReleNumber
    toChange = (255 - OldState) &  BinReleNumber
    #print "toChange" , toChange
    if toChange == 0:
        NeedChange = False
        #print 'already done \n'
        return 'already done', 201, {'Access-Control-Allow-Origin': '*'} 
    else:
        #print 'NeedChange'
        NeedChange = True
        bus20.write_byte_data(DEVICE20,OLATA,toChange)
            
    time.sleep(0.3)
    bus20.write_byte_data(DEVICE20,OLATA,0)
    time.sleep(0.3)
    NewState = bus20.read_byte_data(DEVICE20,GPIOB)
    #print NewState
    #print OldState
    if NeedChange:
        if NewState != OldState:
            return 'ok', 201, {'Access-Control-Allow-Origin': '*'} 
        else:
            return 'malfunction', 201, {'Access-Control-Allow-Origin': '*'} 

@app.route('/reletoggle/<int:number>')
def api_reletoggle(number):
    if number > 8 or number < 1:
        #print 'this rele not exist \n'
        return 'error', 201, {'Access-Control-Allow-Origin': '*'} 
    NeedChange = False
    OldState = bus20.read_byte_data(DEVICE20,GPIOB)
    BinReleNumber = 2** (number - 1)
    #print 'number ' + str(number) + '\n'
    #print 'OldState ' + str(OldState) + '\n'
    #print 'BinReleNumber ' + str(BinReleNumber) + '\n'
    #print 'toggle'
    bus20.write_byte_data(DEVICE20,OLATA,BinReleNumber)
    time.sleep(0.1)
    bus20.write_byte_data(DEVICE20,OLATA,0)
    time.sleep(0.1)
    #test if rele has changed
    NewState = bus20.read_byte_data(DEVICE20,GPIOB)
    #print NewState
    #print OldState
    if OldState != NewState:
        return 'ok', 201, {'Access-Control-Allow-Origin': '*'} 
    else:
        return "malfunction", 201, {'Access-Control-Allow-Origin': '*'} 
    
@app.route('/reledimmon/<int:number>')
def api_reledimmon(number):
    if number > 8 or number < 1:
        #print 'this rele not exist \n'
        return 'error', 201, {'Access-Control-Allow-Origin': '*'} 
    BinReleNumber = 2** (number - 1)
    #print "BinReleNumber",BinReleNumber
    bus20.write_byte_data(DEVICE20,OLATA,BinReleNumber)
    return 'ok', 201, {'Access-Control-Allow-Origin': '*'} 

@app.route('/reledimmoff/<int:number>')
def api_reledimmoff(number):
    if number > 8 or number < 1:
        #print 'this rele not exist \n'
        return 'error', 201, {'Access-Control-Allow-Origin': '*'} 
    bus20.write_byte_data(DEVICE20,OLATA,0)
    lastStateDimm = 0
    return 'ok', 201, {'Access-Control-Allow-Origin': '*'} 

@app.route('/reletimer/<int:number>/<int:unlock_after_millisec>')
def api_reletimer(number,unlock_after_millisec):
    milliseconds = 0.0
    milliseconds = float(unlock_after_millisec) / 1000.0
    if number > 8 or number < 1:
        #print 'this rele not exist \n'
        return 'error', 201, {'Access-Control-Allow-Origin': '*'} 
    BinReleNumber = 2** (number - 1)
    bus20.write_byte_data(DEVICE20,OLATA,BinReleNumber)
    time.sleep(milliseconds)
    bus20.write_byte_data(DEVICE20,OLATA,0)
    return "ok" , 201, {'Access-Control-Allow-Origin': '*'} 

@app.route('/relestate/<int:number>')
def api_relestate(number):
    if number > 8 or number < 1:
        #print 'this rele not exist \n'
        return 'error', 201, {'Access-Control-Allow-Origin': '*'} 
    OldState = bus20.read_byte_data(DEVICE20,GPIOB)
    BinReleNumber = 2** (number - 1)
    #is already on ?
    if BinReleNumber & OldState == BinReleNumber:
        return 'off', 201, {'Access-Control-Allow-Origin': '*'} 
    else:
        return 'on', 201, {'Access-Control-Allow-Origin': '*'} 

@app.route('/relestateall/')
def api_relestateall():
    State = bus20.read_byte_data(DEVICE20,GPIOB)
    #BinReleNumber = bin(OldState)
    #print State
    ##print BinReleNumber
    return str(State), 201, {'Access-Control-Allow-Origin': '*'} 
    
if __name__ == '__main__':
    app.run(host='192.168.0.202',debug = True)
