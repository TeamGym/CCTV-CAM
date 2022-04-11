import socket, pickle

HOST = '192.168.0.13'
PORT = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

data = s.recv(4096)
data = pickle.loads(data)

print(data)
