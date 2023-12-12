from picamera2 import Picamera2
from time import sleep

picam2_0 = Picamera2(0)
picma2_1 = Picamera2(1)

picam2_0.video_configuration.controls.FrameRate = 90.0

config = picam2_0.create_video_configuration(main ={"format": "XBGR8888", "size": (640,480)})
config = picam2_1.create_video_configuration(main ={"format": "XBGR8888", "size": (640,480)})


picam2_0.configure(config)
picam2_1.configure(config)

picam2_0.start_and_record_video("test_0.mp4")
picam2_1.start_and_record_video("test_1.mp4")

sleep(10)

picam2_0.stop_recording()
picam2_1.stop_recording()

exit()