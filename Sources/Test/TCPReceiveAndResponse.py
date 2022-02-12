import socket
import dill

HOST = 'localhost'
PORT = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    try:
        data = s.recv(1024)
        data = dill.loads(data)

        print(data)

        message = "OK"
        message = dill.dumps(message)

        s.send(message)
        
    except KeyboardInterrupt:        
        s.close()
        
        break


