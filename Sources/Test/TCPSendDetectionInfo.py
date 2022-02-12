
import socket, pickle

from DetectionResult import DetectionResult

HOST = '192.168.0.13'
PORT = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)

conn, addr = s.accept()

result = DetectionResult(100, [1, 2, 3])
data = pickle.dumps(result)

conn.send(data)
conn.close()

s.shutdown(socket.SHUT_RDWR)
s.close()

