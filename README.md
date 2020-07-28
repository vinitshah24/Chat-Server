# Sockets Chat Room
TCP server-client network built using Python's socket and library. 
The server listens for new connections and incoming data from each client.

## Run:
### Server
```python
python server.py
```
### Client 1
```python
python client.py
```

### Client 2
```python
python client.py
```
## Output:
### Server
```
Listening on 127.0.0.1 Port 8080...
Message Header: b'5         '
Message Length: 5
User Message: b'Vinit'
Connection Accepted from 127.0.0.1:62307, username: Vinit
Message Header: b'3         '
Message Length: 3
User Message: b'Sam'
Connection Accepted from 127.0.0.1:62308, username: Sam
Message Header: b'6         '
Message Length: 6
User Message: b'Hello!'
Recieved Message -> Vinit: Hello!
Message Header: b'3         '
Message Length: 3
User Message: b'Hi!'
Recieved Message -> Sam: Hi!
```

## Client 1
```
Username: Vinit 
Vinit > Hello!
Vinit > 
```

## Client 2
```
Username: Sam
Sam > 
Vinit > Hello!
Sam > Hi!
Sam > 
```