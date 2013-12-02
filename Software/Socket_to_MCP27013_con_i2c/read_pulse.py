
import smbus
import time
import urllib
import urllib2

bus = smbus.SMBus(1) # Rev 2 Pi uses 1
DEVICE = 0x20 # Device address (A0-A2)
IODIRA = 0x00 # Pin direction register
OLATA  = 0x14 # Register for outputs
GPIOA  = 0x12 # Register for output
GPIOB  = 0x13 # Register for inputs
#variables
OldState = 0x00
ButtonState = False
urlForToggle = 'http://192.168.0.202:5000/reletoggle/2'

while True:
   try: NewState = bus.read_byte_data(DEVICE,GPIOB)
   if (NewState == 1 or NewState == 3) and OldState != NewState:
               #data = urllib.urlencode({'pushtext': str(message),'title': str(title)})
               #req = urllib2.Request(urlForNotification,data)
               response = urllib2.urlopen(urlForToggle)
               html = response.read()
               OldState = NewState
   else:
       OldState = 0x00
       #print 'NewState != OldState %s' , NewState
   #OldState = bus.read_byte_data(DEVICE,GPIOB)
