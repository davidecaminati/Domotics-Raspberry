import smbus
import time
import urllib
import urllib2
 
 
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
#output
bus = smbus.SMBus(1)  # Rev 1 Pi uses 0
#bus = smbus.SMBus(1) # Rev 2 Pi uses 1
 
DEVICE = 0x24 # Device address (A0-A2)
IODIRA = 0x00 # Pin direction register for port A
IODIRB = 0x01 # Pin direction register for port B
OLATA  = 0x14 # Register for outputs for port A
OLATB  = 0x15 # Register for outputs for port B
GPIOA  = 0x12 # Register for inputs for port A
GPIOB  = 0x13 # Register for inputs for port B
GPPUA  = 0x0C # Pull-up resistor (0 = disabled, 1 = enabled)
# Set all GPA pins as outputs by setting
# all bits of IODIRA register to 0
bus.write_byte_data(DEVICE,IODIRB,0)

#Url for change state of reles
urlForToggle = 'http://192.168.0.202:5000/reletoggle/'
#Url for read state of reles
urlForState = 'http://192.168.0.202:5000/relestate/'

# Set output all 7 output bits to 0
bus.write_byte_data(DEVICE,OLATB,0)

# Set PullUp resistor for input register
bus.write_byte_data(DEVICE,GPPUA,255)


def LED1red():
    bus.write_byte_data(DEVICE,OLATB,1)
    #time.sleep(2)

def LED1green():
    bus.write_byte_data(DEVICE,OLATB,2)
    #time.sleep(2)
 

def CheckColorForLed(LedNum):
    #read state
    response = urllib2.urlopen(urlForState + str(LedNum))
    html = response.read()
    #print html
    #time.sleep(8000)
    if html == "on":
        x = LED1green()
        color = "green"
    else:
        x = LED1red()
        color = "red"


x = CheckColorForLed(4)
#color = "red"
bus.write_byte_data(DEVICE,IODIRA,0xFF)
button1oldstate = False
i = 0
# Loop until user presses CTRL-C
while True:
 
    # Read state of GPIOA register
    MySwitch = bus.read_byte_data(DEVICE,GPIOA)
    print MySwitch
    if MySwitch == 254 :
        if button1oldstate == False:
            # send toggle
            response = urllib2.urlopen(urlForToggle + "4")
            html = response.read()
            time.sleep(0.2)
            CheckColorForLed(4)
            button1oldstate = True
    else:
        if button1oldstate == True:
            button1oldstate = False
    time.sleep(0.1)
    # periodic update led state
    i +=1
    if i > 100:
        i = 0 
        CheckColorForLed(4)