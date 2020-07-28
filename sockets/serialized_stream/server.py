import socket
import pickle

HEADER_SIZE = 10
# Creating a socket with IPv4 and TCP stream
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Binding to the host IP and port
s.bind((socket.gethostname(), 8080))
# Allocating the Queue size
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f'Connection Established from {address}')
    obj = {1: 'USA', 2: 'India'}
    message = pickle.dumps(obj)
    # Adding Header (empty spaces to fill up len) with message
    message = bytes(f'{len(message):<{HEADER_SIZE}}', 'utf-8') + message
    # Send data to the client
    clientsocket.send(message)
