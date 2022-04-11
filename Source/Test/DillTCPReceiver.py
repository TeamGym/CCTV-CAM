import socket
import dill

HOST = 'localhost'
PORT = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

data = s.recv(4096)
instance = dill.loads(data)

print(instance)
print(instance.a)
print(instance.b)
print(instance.dillInnerInstance)
