import smbus
import time
 
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
 
# Set all GPA pins as outputs by setting
# all bits of IODIRA register to 0
bus.write_byte_data(DEVICE,IODIRB,0)
 
# Set output all 7 output bits to 0
bus.write_byte_data(DEVICE,OLATB,0)
 
def LED1red():
    bus.write_byte_data(DEVICE,OLATB,1)
    #time.sleep(2)

def LED1green():
    bus.write_byte_data(DEVICE,OLATB,2)
    #time.sleep(2)
 
color = "red"
bus.write_byte_data(DEVICE,IODIRA,0x80)
button1oldstate = False
# Loop until user presses CTRL-C
while True:
 
    # Read state of GPIOA register
    MySwitch = bus.read_byte_data(DEVICE,GPIOA)
    print MySwitch
    if MySwitch == 1 :
        if button1oldstate == False:
            if color == "red":
                x = LED1green()
                color = "green"
            else:
                x = LED1red()
                color = "red"
            print "Switch was pressed!"
            button1oldstate = True
    else:
        if button1oldstate == True:
            button1oldstate = False
    time.sleep(0.1)