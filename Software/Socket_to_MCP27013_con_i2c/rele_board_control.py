from flask import Flask, url_for
import smbus
import time

bus = smbus.SMBus(1) # Rev 2 Pi uses 1
DEVICE = 0x20 # Device address (A0-A2)
IODIRA = 0x00 # Pin direction register
OLATA  = 0x14 # Register for outputs
GPIOA  = 0x12 # Register for output
GPIOB  = 0x13 # Register for inputs
bus.write_byte_data(DEVICE,IODIRA,0x00)
app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/releon/<int:number>')
def api_articles(number):
    OldState = bus.read_byte_data(DEVICE,GPIOB)
    #BinOldState = bin(OldState)
    NeedChangeState = False
    StateChanged = False
    BinReleNumber = 2** (number - 1)
    #x = bin(BinReleNumber) -  bin(BinOldState)
    #print x
    if OldState == '0b0':
        print 'old state is all off'
        NeedChangeState = True
        bus.write_byte_data(DEVICE,OLATA,BinReleNumber)
    else:
        #is already on ?
        print 'number ' + str(number)
        print 'OldState ' + str(OldState)
        print 'BinReleNumber ' + str(BinReleNumber)
        if BinReleNumber & OldState == BinReleNumber:
            print 'already done'
        else:
#            NewConfiguration = BinReleNumber | OldState
#            print 'NewConfiguration ' + str(NewConfiguration)
            bus.write_byte_data(DEVICE,OLATA,BinReleNumber)
    time.sleep(0.3)
    bus.write_byte_data(DEVICE,OLATA,0)
    time.sleep(0.5)
    NewState = bus.read_byte_data(DEVICE,GPIOB)
    return 'ok'

@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'You are reading ' + articleid

if __name__ == '__main__':
    app.run()
