#client example
import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.0.86', 5001))
data = raw_input ( "invia un carattere" )

client_socket.send(data)
client_socket.send("exit")
