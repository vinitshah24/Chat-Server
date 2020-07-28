import socket
import time

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
    message = 'Hello from Socket Server!'
    # Adding Header (empty spaces to fill up len) with message
    message = f'{len(message):<{HEADER_SIZE}}' + message
    # Send data to the client
    clientsocket.send(bytes(message, 'utf-8'))

    while True:
        time.sleep(3)
        msg = f'Current Time is {time.time()}'
        msg = f'{len(msg):<{HEADER_SIZE}}' + msg
        clientsocket.send(bytes(msg, 'utf-8'))
