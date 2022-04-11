import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

GObject.threads_init()
Gst.init(None)

pipeline = Gst.parse_launch("v4l2src name=m_src ! videoconvert ! video/x-raw,width=640,height=480,framerate=30/1,format=I420 ! omxh264enc name=m_encoder ! video/x-h264,stream-format=byte-stream ! rtph264pay name=m_pay ! udpsink name=m_sink")

source = pipeline.get_by_name('m_src')
source.set_property('device', '/dev/video0')

encoder = pipeline.get_by_name('m_encoder')
encoder.set_property('control-rate', 1)

pay = pipeline.get_by_name('m_pay')
pay.set_property('name', 'pay0')
pay.set_property('pt', 96)

sink = pipeline.get_by_name('m_sink')
sink.set_property('host', '127.0.0.1')
sink.set_property('port', 50001)

pipeline.set_state(Gst.State.PLAYING)

loop = GObject.MainLoop()
loop.run()
