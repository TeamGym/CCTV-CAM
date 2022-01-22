sudo modprobe v4l2loopback devices=1 exclusive_caps=1 video_nr=0 card_lable="Webcam"
ffmpeg -i rtsp://snailgod86:wasa4230@192.168.0.17:554/stream1 -f v4l2 -pix_fmt yuv420p /dev/video0
