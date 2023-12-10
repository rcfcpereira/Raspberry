from picamera2 import Picamera2
from time import sleep

picam2 = Picamera2()

config = picam2.create_video_configuration(main ={"format": "XBGR8888", "size": (640,480)})

picam2.video_configuration.controls.FrameRate = 120.0

picam2.configure(config)

picam2.start_and_record_video("test.mp4")

sleep(100)

picam2.stop_recording()

exit()

sleep


