# Render

렌더링을 위한 소스코드가 들어있습니다.

### Window.py

pyglet backend의 기본 윈도우 클래스입니다.
Mouse, Keyboard, System 등 다양한 이벤트에 대한 핸들러(콜백) 시스템을 제공합니다.

### BufferMonitor.py

Buffer에 대한 정보를 담은 클래스입니다.

### RenderableMonitor.py

렌더링하려는 Buffer에 대한 Viewport 역할을 하는 클래스입니다.

### BufferRenderer.py

멀티 버퍼 렌더링을 지원하는 클래스입니다.

### BufferViewer.py

BufferRenderer를 상속받아 멀티 버퍼 렌더링
