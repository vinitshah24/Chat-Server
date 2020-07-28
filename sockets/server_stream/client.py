
import socket

# Creating a socket with IPv4 and TCP stream
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connecting to the host IP and port
s.connect((socket.gethostname(), 8080))

full_msg = ''
while True:
    # Allocating the buffer to recieve the stream of data
    msg = s.recv(10)
    if len(msg) <= 0:
        break
    full_msg += msg.decode('utf-8')
print(full_msg)
