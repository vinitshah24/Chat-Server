import socket

# Creating a socket with IPv4 and TCP stream
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Binding to the host IP and port
s.bind((socket.gethostname(), 8080))
# Allocating the Queue size
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f'Connection Established from {address}')
    # Send data to the client
    clientsocket.send(bytes('Hello from Socket Server!', 'utf-8'))
    clientsocket.close()
