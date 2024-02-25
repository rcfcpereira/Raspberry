# library.py

import os
import time
import RPi.GPIO as GPIO
from picamera2 import Picamera2
from picamera2.encoders import MultiEncoder
from PIL import Image, ImageDraw, ImageFont
import threading

# Define lcd gpio configuration:
RST = 27
DC = 25
BL = 24
bus = 0
device = 0

disp = LCD_2inch4.LCD_2inch4(spi=SPI.SpiDev(bus, device), spi_freq=40000000, rst=RST, dc=DC, bl=BL)
# Initialize library.
disp.Init()
# Clear display.
disp.clear()
# Display DutyCycle
disp.bl_DutyCycle(100)
# Set Fonts
Font1 = ImageFont.truetype("Font/Font02.ttf", 30)
Font2 = ImageFont.truetype("Font/Font02.ttf", 24)
Font3 = ImageFont.truetype("Font/Font02.ttf", 15)
Font4 = ImageFont.truetype("Font/Font02.ttf", 100)

time.sleep(1)

# Function to rotate screen and send to display
def rotate_print(image):
    im_r = image.rotate(180)
    disp.ShowImage(im_r)

# Define interrupt handler and other variables
racer_left_start_time = 0
racer_right_start_time = 0
racer_left = False
racer_right = False
racer_left_finish_time = 0
racer_right_finish_time = 0
racer_left_cross = False
racer_right_cross = False
time_stamp_start = 0

def false_start_left(channel):
    global racer_left_start_time
    racer_left_start_time = time.process_time_ns()

def false_start_right(channel):
    global racer_right_start_time
    racer_right_start_time = time.process_time_ns()

def left_lane(channel):
    global racer_left_finish_time
    global racer_left_cross
    racer_left_finish_time = time.process_time_ns()
    racer_left_cross = True

def right_lane(channel):
    global racer_right_finish_time
    global racer_right
    racer_right_finish_time = time.process_time_ns()
    racer_right = True

def start_camera(camera, filename):
    if os.path.exists(filename):
        choice = input("File already exists. Do you want to add information (A) or replace the file (R)? ").upper()
        if choice == "A":
            camera.start_and_record_video(filename, append=True)
        elif choice == "R":
            camera.start_and_record_video(filename)
        else:
            print("Invalid choice. Defaulting to replacing the file.")
            camera.start_and_record_video(filename)
    else:
        camera.start_and_record_video(filename)

def write_race_time(draw, font, time_stamp_start, time_stamp_finish, racer_start_time, racer_finish_time, racer_name, position):
    if racer_start_time == 0:
        draw.text((20, position), "{} Start: False Start".format(racer_name), fill="RED", font=font)
    else:
        race_time = (racer_finish_time - time_stamp_start) / 1000000000
        draw.text((20, position), "{} Start: {:.3f} s (Finish: {:.3f} s)".format(racer_name, race_time, (time_stamp_finish - time_stamp_start) / 1000000000), fill="RED", font=font)
