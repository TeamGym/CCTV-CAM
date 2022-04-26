# CCTV-CAM

CCTV 시스템 개발 파트 중 CCTV 임베디드 장비 개발 파트입니다.

## 제공하는 기능

### Video Capturing
    설정값을 이용하여 카메라에서 프레임을 받아옵니다.

### Video Recording
    설정값의 clip length에 따라 받아온 영상을 잘라서 보관합니다.

### Object Detection
    Object Detection Model을 활용하여 실시간으로 영상을 분석합니다.

### Motion Detection
    받아온 프레임들을 비교하여 Motion이 발생하였는지 분석합니다.

### TCP Networking
    서버와 TCP 프로토콜을 사용하여 정보를 주고받습니다.

### Video Streaming
    RTP 혹은 RTSP를 사용해 실시간으로 영상을 전송합니다.

### Audio Streaming
    RTP 혹은 RTSP를 사용해 실시간으로 음성을 전송합니다.

### Device Control
    프로그램 또는 서버에서 연결된 장치를 컨트롤합니다.

### Audio Alert
    내장된 오프라인 TTS Engine을 이용하여 특정 신호 발생 시 음성으로 경고를 합니다.

### Realtime Logging
    Detection Result 등을 실시간으로 로깅합니다.

### Rendering
    영상이나 Detection Result 등 원하는 데이터를 화면에 렌더링합니다.
