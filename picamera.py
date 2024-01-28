from picamera2 import Picamera2
from picamera2.encoders import MultiEncoder
from time import sleep

# picam2 = Picamera2(0)

# picam2.configure(picam2.create_video_configuration(main = {"size" : (640,480)}, controls  = {'FrameRate': 200}))

# picam2.start_and_record_video("test.mp4", duration = 60)

# picam2 = Picamera2(0)
# sensor_modes = picam2.sensor_modes

# picam2 = Picamera2(1)
# sensor_modes = picam2.sensor_modes

#Set Camare settings
picam2_0 = Picamera2(0)
picam2_1 = Picamera2(1)
encoder = MultiEncoder()

config_0 = picam2_0.create_video_configuration(main = {"size" : (640,480), "format" : "RGB888"}, controls  = {'FrameRate': 120})
config_1 = picam2_1.create_video_configuration(main = {"size" : (640,480), "format" : "RGB888"}, controls  = {'FrameRate': 120})

picam2_0.configure(config_0)
picam2_1.configure(config_1)

picam2_0.start_and_record_video("left_track.mp4")
picam2_1.start_and_record_video("rigth_track.mp4")

sleep(5)

picam2_0.stop_recording()
picam2_1.stop_recording()