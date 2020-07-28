import socket
import select
import errno
import sys

IP = "127.0.0.1"
PORT = 8080
HEADER_SIZE = 10

client_user = input("Username: ")

# Creating a socket with IPv4 and TCP stream
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connecting to a given IP and port
client.connect((IP, PORT))
# Set connection to non-blocking state so .recv() call won't block
client.setblocking(False)

# Preparing username & header to send
username = client_user.encode('utf-8')
username_header = f"{len(username):<{HEADER_SIZE}}".encode('utf-8')
# Sending the data to server
client.send(username_header + username)

while True:
    # Wait for user to input a message
    message = input(f'{client_user} > ')
    # If message exists then send
    if message:
        # Encode message to bytes, prepare header and convert to bytes
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_SIZE}}".encode('utf-8')
        # Sending the data to server
        client.send(message_header + message)
    try:
        # loop over received messages
        while True:
            # Receive the header containing username length
            username_header = client.recv(HEADER_SIZE)
            # If we received no data, server might be closed
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())
            # Receive and decode username
            username = client.recv(username_length).decode('utf-8')
            # As we received username, we received whole message,
            # So no need to check if it has any length
            message_header = client.recv(HEADER_SIZE)
            message_length = int(message_header.decode('utf-8').strip())
            message = client.recv(message_length).decode('utf-8')
            # Print message
            print(f'{username} > {message}')

    except IOError as e:
        # Exception raised for non blocking connections when there's no incoming data
        # If any different error code then error might have occured
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
        # No new incoming data so continue
        continue

    except Exception as e:
        # Any other exception - something happened, exit
        print('Exception Raised: {}'.format(str(e)))
        sys.exit()
