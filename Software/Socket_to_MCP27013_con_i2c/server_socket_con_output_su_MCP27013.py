import smbus
import time

bus = smbus.SMBus(1) # Rev 2 Pi uses 1

DEVICE = 0x20 # Device address (A0-A2)
IODIRA = 0x00 # Pin direction register
OLATA  = 0x14 # Register for outputs
GPIOA  = 0x12 # Register for inputs

# Set all GPA pins as outputs by setting
# all bits of IODIRA register to 0
bus.write_byte_data(DEVICE,IODIRA,0x00)

# Set output all 7 output bits to 0
bus.write_byte_data(DEVICE,OLATA,0)

from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys
PORT_NUMBER = 5000
SIZE = 1024

hostName = gethostbyname( '192.168.0.202' )
mySocket = socket( AF_INET,SOCK_DGRAM)
mySocket.bind( (hostName, PORT_NUMBER) )

print ("Test server listening on port {0}\n".format(PORT_NUMBER))
ext = 0
while ext == 0:
    (data,addr) = mySocket.recvfrom(SIZE)
    bus.write_byte_data(DEVICE,OLATA,int(data))
    if data == "155":
        ext = 1
bus.write_byte_data(DEVICE,OLATA,1)
  
# Set all bits to zero
bus.write_byte_data(DEVICE,OLATA,0)
sys.ext()
