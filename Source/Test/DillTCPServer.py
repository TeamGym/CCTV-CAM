import socket
import dill

class DillClass:
    def __init__(self, a, b, dillInnerClass):
        self.a = a
        self.b = b

        self.dillInnerInstance = dillInnerClass

class DillInnerClass:
    def __init__(self):
        pass

HOST = 'localhost'
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)

conn, addr = s.accept()

instance = DillClass(10, "dill", DillInnerClass())
data = dill.dumps(instance)

conn.send(data)
conn.close()

s.shutdown(socket.SHUT_RDWR)
s.close()

