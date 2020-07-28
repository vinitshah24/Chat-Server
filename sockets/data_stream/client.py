import socket

HEADER_SIZE = 10
# Creating a socket with IPv4 and TCP stream
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connecting to the host IP and port
s.connect((socket.gethostname(), 8080))

while True:
    full_msg = ''
    new_msg = True
    while True:
        # Allocating the buffer to recieve the stream of data
        msg = s.recv(16)
        if new_msg:
            msg_len = int(msg[:HEADER_SIZE])
            new_msg = False
            print('New Message Length: ', int(msg[:HEADER_SIZE]))
            print(f'Message Length: {msg_len - HEADER_SIZE}')
        full_msg += msg.decode('utf-8')
        if len(full_msg) - HEADER_SIZE == msg_len:
            print(f'Recieved Message: {full_msg[HEADER_SIZE:]}\n')
            new_msg = True
            full_msg = ''
