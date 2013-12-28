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
GPPUB  = 0x0D # Pull-up resistor (0 = disabled, 1 = enabled)
# Set all GPA pins as outputs by setting
# all bits of IODIRA register to 0
bus.write_byte_data(DEVICE,IODIRB,0x00)

bus.write_byte_data(DEVICE,IODIRA,0x3f)

#Url for change state of reles
urlForToggle = 'http://192.168.0.202:5000/reletoggle/'
#Url for read state of rele
urlForState = 'http://192.168.0.202:5000/relestate/'
#Url for read state of all reles
urlForStateAll = 'http://192.168.0.202:5000/relestateall/'

# Set output all 7 output bits to 0
bus.write_byte_data(DEVICE,OLATB,0x00)
# Set PullUp resistor for input register
bus.write_byte_data(DEVICE,GPPUA,0xFF) #11111111
bus.write_byte_data(DEVICE,GPPUB,0xFF) #11111111
#for p in [1,2,4,8,16,32]:
#    bus.write_byte_data(DEVICE,OLATB,32)
#    time.sleep(3)
#time.sleep (1000)
RELE_INGRESSO = 4
RELE_CUCINA = 8
RELE_SALA = 16

#color for led
bus.write_byte_data(DEVICE,GPIOB,0b101010)

#reset button state
button1oldstate = False
button2oldstate = False
button3oldstate = False

def LEDCucinaRed():
    OldState = bus.read_byte_data(DEVICE,GPIOB)
    BinLedNumberRED = 0b00000001
    BinLedNumberGREEN = 0b00000010
    NewBinLedNumber =  (OldState & ( ~ BinLedNumberGREEN )) | BinLedNumberRED
    bus.write_byte_data(DEVICE,GPIOB,NewBinLedNumber)
def LEDCucinaGreen():
    OldState = bus.read_byte_data(DEVICE,GPIOB)
    BinLedNumberRED = 0b00000001
    BinLedNumberGREEN = 0b00000010
    NewBinLedNumber =  (OldState & ( ~ BinLedNumberRED)) | BinLedNumberGREEN
    bus.write_byte_data(DEVICE,GPIOB,NewBinLedNumber)
def LEDIngressoRed():
    OldState = bus.read_byte_data(DEVICE,GPIOB)
    BinLedNumberRED = 0b00000100
    BinLedNumberGREEN = 0b00001000
    NewBinLedNumber =  (OldState & ( ~ BinLedNumberGREEN)) | BinLedNumberRED
    bus.write_byte_data(DEVICE,GPIOB,NewBinLedNumber)
def LEDIngressoGreen():
    OldState = bus.read_byte_data(DEVICE,GPIOB)
    BinLedNumberRED = 0b00000100
    BinLedNumberGREEN = 0b00001000
    NewBinLedNumber =  (OldState & ( ~ BinLedNumberRED)) | BinLedNumberGREEN
    bus.write_byte_data(DEVICE,GPIOB,NewBinLedNumber)
def LEDSalaRed():
    OldState = bus.read_byte_data(DEVICE,GPIOB)
    BinLedNumberRED = 0b00010000
    BinLedNumberGREEN = 0b00100000
    NewBinLedNumber =  (OldState & ( ~ BinLedNumberGREEN)) | BinLedNumberRED
    bus.write_byte_data(DEVICE,GPIOB,NewBinLedNumber)
def LEDSalaGreen():
    OldState = bus.read_byte_data(DEVICE,GPIOB)
    BinLedNumberRED = 0b00010000
    BinLedNumberGREEN = 0b00100000
    NewBinLedNumber =  (OldState & ( ~ BinLedNumberRED)) | BinLedNumberGREEN
    bus.write_byte_data(DEVICE,GPIOB,NewBinLedNumber)

def CheckColorForLeds():
    #read state
    response = urllib2.urlopen(urlForStateAll)
    html = response.read()
    statevalue = int(html)
    time.sleep(0.2)
    
    if (statevalue & RELE_CUCINA) == RELE_CUCINA:
        x = LEDCucinaGreen()
    else:
        x = LEDCucinaRed()
        
    if (statevalue & RELE_INGRESSO) == RELE_INGRESSO:
        x = LEDIngressoGreen()
    else:
        x = LEDIngressoRed()
        
    if (statevalue & RELE_SALA) == RELE_SALA:
        x = LEDSalaGreen()
    else:
        x = LEDSalaRed()

i = 0
x = CheckColorForLeds()

# Loop until user presses CTRL-C
while True:
 
    # Read state of GPIOA register
    MySwitch = bus.read_byte_data(DEVICE,GPIOA)
    #print "MySwitch %s" % MySwitch
    if MySwitch == 62 :
        if button1oldstate == False:
            # send toggle
            response = urllib2.urlopen(urlForToggle + "4")
            html = response.read()
            time.sleep(0.2)
            CheckColorForLeds()
            button1oldstate = True
            #print "RELE_CUCINA"
    if MySwitch == 61 :
        if button2oldstate == False:
            # send toggle
            response = urllib2.urlopen(urlForToggle + "3")
            html = response.read()
            time.sleep(0.2)
            CheckColorForLeds()
            button2oldstate = True
            #print "RELE_INGRESSO"
    if MySwitch == 59 :
        if button3oldstate == False:
            # send toggle
            response = urllib2.urlopen(urlForToggle + "5")
            html = response.read()
            time.sleep(0.2)
            CheckColorForLeds()
            button3oldstate = True
            #print "RELE_SALA"
    else:
        if button1oldstate == True:
            button1oldstate = False
        if button2oldstate == True:
            button2oldstate = False
        if button3oldstate == True:
            button3oldstate = False
    time.sleep(0.1)
    # periodic update led state
    i +=1
    if i > 100:
        i = 0 
        CheckColorForLeds()
