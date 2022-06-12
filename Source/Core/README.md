# Core

코어 라이브러리 입니다.

### Buffer.py

기본적인 버퍼 클래스입니다.

### BufferHolder.py

여러 버퍼를 이름으로 등록하고 쿼리할 수 있는 클래스입니다.

### BufferBroadcaster.py

BufferHolder를 상속한 클래스로, Buffer처럼 push 할 수 있으며,
등록된 버퍼들에 push된 데이터를 broadcast 합니다.

### Frame.py

timestamp, data로 구성된 Video Frame 클래스입니다.

### JSON.py

JSON 파일을 로드할 때 사용되는 클래스입니다.
