from picamera2 import Picamera2

picam2 = Picamera2(1)

picam2.configure(picam2.create_video_configuration(main = {"size" : (640,480)}, controls  = {'FrameRate': 200}))

picam2.start_and_record_video("test.mp4", duration = 60)