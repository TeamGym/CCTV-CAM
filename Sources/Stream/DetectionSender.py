import time

class DetectionSender:
    def __init__(self,
                 host : str,
                 port : int):
        
        self.host = host
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
        self.socket.settimeout(10)
        
        self.latestTimestamp = 0

    def connect():
        while not self.socket.connect_ex((self.host, self.port)):
            print("[DetectionSender]: Can't connect server, wait 3 second.")
            time.sleep(3)

    def start():
        cctvInfo = {
            "cam_id": 0,
            "mode": 1,
        }
        cctvInfo = json.dumps(cctvInfo)

        self.socket.sendall(cctvInfo)

        while True:
            if self.detectionResultBuffer.size <= 0:
                continue

            detectionResult = self.detectionResultBuffer.tail()            
            timestamp = detectionResult.timestamp            

            if timestamp <= self.latestTimestamp:
                continue

            detectionResult = json.dumps(detectionResult.as_dict)

            data = dill.dumps(detectionResult)
            self.socket.send(data)

            self.latestTimestamp = detectionResult.timestamp

