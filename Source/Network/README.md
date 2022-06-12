# Network

네트워크 통신에 사용되는 소스코드가 들어있습니다.

### ConnectionHolder.py

Connection들의 현재 상태를 담는 클래스입니다.

### ServerStatus.py

현재 서버 상태를 나타내는 enum 클래스입니다.

### RemoteServerConnector.py

중앙 서버와 tcp 프로토콜로 통신하며 stream, request, response를 주고받는 클래스입니다.

### AudioStreamer.py

중앙 서버로 Microphone input을 스트리밍 하는 클래스입니다.

### VideoStreamer.py

중앙 서버로 Video input을 스트리밍 하는 클래스입니다.
