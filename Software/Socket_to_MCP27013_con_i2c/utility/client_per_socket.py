import sys
import argparse
from socket import socket, AF_INET, SOCK_DGRAM


parser = argparse.ArgumentParser()
parser.add_argument("rgb", help="display a square of a given number",type=int)
args = parser.parse_args()
valore = args.rgb
print args.rgb
print type(args.rgb)

SERVER_IP   = '192.168.0.15'
PORT_NUMBER = 5000
SIZE = 1024
print ("Test client sending packets to IP {0}, via port {1}\n".format(SERVER_IP, PORT_NUMBER))

mySocket = socket( AF_INET, SOCK_DGRAM )

while True:
    mySocket.sendto(str(valore),(SERVER_IP,PORT_NUMBER))
sys.exit()
