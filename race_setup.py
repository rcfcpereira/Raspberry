import RPi.GPIO as GPIO
import spidev as SPI
from picamera2 import Picamera2
from picamera2.encoders import MultiEncoder
from lib import LCD_2inch4
import threading
from PIL import Image, ImageDraw, ImageFont

class RaceSetup:
    def __init__(self):
        self.GPIO_initialized = False
        self.display_initialized = False
        self.camera_initialized = False

    def setup_GPIO(self):
        if not self.GPIO_initialized:
            # Define GPIO pins
            self.START_BUTTON_LED = 18
            self.START_BUTTON = 19
            self.SENSOR_START_LEFT = 5
            self.SENSOR_START_RIGHT = 6
            self.START_LIGHT = 26
            self.FALSE_START_LEFT_LED = 22
            self.FALSE_START_RIGHT_LED = 23
            self.SENSOR_FINISH_LEFT = 16
            self.SENSOR_FINISH_RIGHT = 17

            # Set GPIO mode
            GPIO.setmode(GPIO.BCM)

            # Set up GPIO pins
            GPIO.setup(self.SENSOR_START_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.SENSOR_START_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.SENSOR_FINISH_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.SENSOR_FINISH_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.START_LIGHT, GPIO.OUT)
            GPIO.setup(self.START_BUTTON_LED, GPIO.OUT)
            GPIO.setup(self.START_BUTTON, GPIO.IN)
            GPIO.setup(self.FALSE_START_LEFT_LED, GPIO.OUT)
            GPIO.setup(self.FALSE_START_RIGHT_LED, GPIO.OUT)

            # Set initial states for LEDs
            GPIO.output(self.START_BUTTON_LED, 0)
            GPIO.output(self.START_LIGHT, 0)
            GPIO.output(self.FALSE_START_LEFT_LED, 0)
            GPIO.output(self.FALSE_START_RIGHT_LED, 0)

            self.GPIO_initialized = True

    def setup_display(self):
        if not self.display_initialized:
            # Initialize LCD display
            self.RST = 27
            self.DC = 25
            self.BL = 24
            self.bus = 0
            self.device = 0

            self.disp = LCD_2inch4.LCD_2inch4(spi=SPI.SpiDev(self.bus, self.device), spi_freq=40000000, rst=self.RST, dc=self.DC, bl=self.BL)
            self.disp.Init()
            self.disp.clear()
            self.disp.bl_DutyCycle(100)

            self.display_initialized = True

    def setup_camera_threads(self):
        if not self.camera_initialized:
            self.picam2_0 = Picamera2(0)
            self.picam2_1 = Picamera2(1)

            self.thread_left_camera = threading.Thread(target=self.picam2_0.start_and_record_video, args=("left_track.mp4",))
            self.thread_right_camera = threading.Thread(target=self.picam2_1.start_and_record_video, args=("right_track.mp4",))

            self.thread_left_camera.start()
            self.thread_right_camera.start()

            self.camera_initialized = True

    def setup_camera_config(self):
        if not self.camera_initialized:
            self.encoder = MultiEncoder()
            self.config_0 = self.picam2_0.create_video_configuration(main={"size": (640, 480), "format": "RGB888"}, controls={'FrameRate': 200})
            self.config_1 = self.picam2_1.create_video_configuration(main={"size": (640, 480), "format": "RGB888"}, controls={'FrameRate': 200})
            self.picam2_0.configure(self.config_0)
            self.picam2_1.configure(self.config_1)

            self.camera_initialized = True

    def setup_all(self):
        self.setup_GPIO()
        self.setup_display()
        self.setup_camera_threads()
        self.setup_camera_config()

    def rotate_print(self, image):
        im_r = image.rotate(180)
        self.disp.ShowImage(im_r)
