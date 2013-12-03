import smbus
import time

#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

DEVICE = 0x24 # Device address (A0-A2)
IODIRA = 0x00 # Pin direction register
IODIRB = 0x01 # Pin direction register
OLATA  = 0x14 # Register for outputs
OLATB  = 0x15 # Register for outputs
GPIOA  = 0x12 # Register for inputs
GPIOB  = 0x13 # Register for inputs

# Set first 6 GPA pins as outputs and
# last one as input.
bus.write_byte_data(DEVICE,IODIRB,0x80)

bus.write_byte_data(DEVICE,IODIRA,0x00)
#time.sleep(1)
bus.write_byte_data(DEVICE,OLATA,255)
stato = 0

# Loop until user presses CTRL-C
while True:

  # Read state of GPIOA register
  MySwitch = bus.read_byte_data(DEVICE,GPIOB)
  #print MySwitch
  if MySwitch == 0b10000000 & stato == 0:
  #print "Switch was pressed! 8"
     stato = 1
     bus.write_byte_data(DEVICE,OLATA,0)
     #stato = 0
     time.sleep(1)
     bus.write_byte_data(DEVICE,OLATA,255)
     #stato = 0
  #if MySwitch == 0b01000000:
  #print "Switch was pressed! 7"
  #   bus.write_byte_data(DEVICE,OLATA,0)

