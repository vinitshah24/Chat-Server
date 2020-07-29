import socket
import select

IP = "127.0.0.1"
PORT = 8080
HEADER_SIZE = 10

# Creating a socket with IPv4 and TCP stream
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Set the socket options
# SOL_SOCKET    = Socket option LEVEL
# SO_REUSEADDR  = Socket option NAME - allow reuse of local addresses
# Socket Value  = Sets socket option to 1 on SO_REUSEADDR
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Binding to the host IP and port
server.bind((IP, PORT))
# Listening to new connections
server.listen()
print(f'Listening on {IP} Port {PORT}...')

# List of sockets for select.select()
SOCKET_LIST = [server]
# key=socket, value= Header and username
CLIENTS = {}


def receive_message(client_sock):
    try:
        # Receive our "header" containing message length
        message_header = client_sock.recv(HEADER_SIZE)
        print(f"Message Header: {message_header}")
        # If no data is reveived
        if not len(message_header):
            return False
        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())
        print(f"Message Length: {message_length}")
        user_message = client_sock.recv(message_length)
        print(f"User Message: {user_message}")
        # Return an object of message header and message data
        return {'header': message_header, 'data': user_message}
    except:
        return False


while True:
    # select.select() calls Unix or Windows select() call
    readable, writable, exceptional = \
        select.select(SOCKET_LIST, [], SOCKET_LIST)

    for notified_socket in readable:
        # If notified socket is a server socket -> new connection, accept it
        if notified_socket == server:
            # Accepting new connection (Client Socket)
            client_socket, client_address = server.accept()
            # Receiving Clinet's username
            user = receive_message(client_socket)
            # If the client disconnected before sending the username
            if user is False:
                continue
            # Adding the accepted socket to SOCKET list
            SOCKET_LIST.append(client_socket)
            # Saving the and username header and username
            CLIENTS[client_socket] = user

            print('Connection Accepted from {}:{}, username: {}'
                  .format(*client_address, user['data'].decode('utf-8')))

        # Existing socket might be sending a message
        else:
            # Receive the message
            message = receive_message(notified_socket)
            # If Client disconnected then Cleanup
            if message is False:
                print('Connection closed from: {}'
                      .format(CLIENTS[notified_socket]['data'].decode('utf-8')))
                # Remove from list for SOCKET LIST
                SOCKET_LIST.remove(notified_socket)
                # Remove from CLIENT list
                del CLIENTS[notified_socket]
                continue

            # Get user by notified socket, so we will know who sent the message
            user = CLIENTS[notified_socket]

            print('Recieved Message -> {}: {}'
                  .format(user["data"].decode("utf-8"),
                          message["data"].decode("utf-8")))

            # Iterate over connected CLIENTS and broadcast the messages
            for client_socket in CLIENTS:
                # Don't send it to the sender
                if client_socket != notified_socket:
                    # Send user and message
                    client_socket.send(user['header'] + user['data'] +
                                       message['header'] + message['data'])

    # Handling Socket Exceptions
    for e in exceptional:
        SOCKET_LIST.remove(e)
        del CLIENTS[e]
