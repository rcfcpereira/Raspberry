# main_program.py

import os
import sys
import time
import spidev as SPI
import smbus
import RPi.GPIO as GPIO
from picamera2 import Picamera2
from picamera2.encoders import MultiEncoder
import threading
from lib import LCD_2inch4
from PIL import Image, ImageDraw, ImageFont
import library  # Importing the library functions

# Define Picamera2 instances for left and right cameras
picam2_0 = Picamera2(0)
picam2_1 = Picamera2(1)

# Define GPIOS
# START BUTTON
START_BUTTON_LED = 18
START_BUTTON = 19

# START LINE
SENSOR_START_LEFT = 5
SENSOR_START_RIGHT = 6
START_LIGHT = 26
FALSE_START_LEFT_LED = 22
FALSE_START_RIGHT_LED = 23
# FINISH LINE
SENSOR_FINISH_LEFT = 16
SENSOR_FINISH_RIGHT = 17

# Code
if __name__ == "__main__":
    try:
        # Start Message
        draw.text((75, 5), 'Drag Race', fill="WHITE", font=library.Font1)
        library.rotate_print(image)

        time.sleep(5)

        # Ask for racer names
        racer_name_left = input("Enter the name for the left racer: ")
        racer_name_right = input("Enter the name for the right racer: ")

        # Start Race
        draw.text((55,100), "Press the button", fill="WHITE", font=library.Font2)
        draw.text((55,124), "  to start race ", fill="WHITE", font=library.Font2)
        library.rotate_print(image)

        time.sleep(1)

        GPIO.output(START_BUTTON_LED, 1)

        while True:
            # Press Button to Start Race
            if GPIO.input(START_BUTTON) == 0:
                # Start Camera recording
                left_camera_thread = threading.Thread(target=library.start_camera, args=(picam2_0, "left_track.mp4"))
                right_camera_thread = threading.Thread(target=library.start_camera, args=(picam2_1, "right_track.mp4"))

                left_camera_thread.start()
                right_camera_thread.start()

                GPIO.add_event_detect(SENSOR_START_LEFT, GPIO.FALLING, callback=library.false_start_left, bouncetime=10)
                GPIO.add_event_detect(SENSOR_START_RIGHT, GPIO.FALLING, callback=library.false_start_right, bouncetime=10)

                GPIO.add_event_detect(SENSOR_FINISH_LEFT, GPIO.FALLING, callback=library.left_lane, bouncetime=10)
                GPIO.add_event_detect(SENSOR_FINISH_RIGHT, GPIO.FALLING, callback=library.right_lane, bouncetime=10)

                draw.rectangle([(0,100),(240,320)], fill="BLACK")
                draw.text((60,100), " Race Start in: ", fill="WHITE", font=library.Font2)
                library.rotate_print(image)

                for x in range(6):
                    draw.rectangle([(95,124),(195,224)], fill="BLACK")
                    draw.text((94,124), "{}".format(str((5-x))), fill="RED", font=library.Font4)
                    library.rotate_print(image)
                    time.sleep(1)

                    if library.racer_left_start_time != 0:
                        GPIO.output(FALSE_START_LEFT_LED, 1)
                    if library.racer_right_start_time != 0:                 
                        GPIO.output(FALSE_START_RIGHT_LED, 1)

                clock = 0
                library.time_stamp_start = time.process_time_ns()
                GPIO.output(START_LIGHT, 1)

                break

        draw.rectangle([(0,100),(240,320)], fill="BLACK")
        draw.text((15,100), "TIME:", fill="WHITE", font=library.Font2)

        # Disable start sensor's
        START_SENSORS = SENSOR_START_LEFT, SENSOR_START_RIGHT
        GPIO.cleanup(START_SENSORS)

        while (library.racer_left != True and library.racer_right != True):

            draw.rectangle([(20,124),(240,148)], fill="BLACK")
            draw.text((20,124), "{:.3f} s".format(clock), fill="RED", font=library.Font2)
            library.rotate_print(image)
            clock = (time.process_time_ns() - library.time_stamp_start) / 1000000000

            time.sleep(0.01)

        time_stamp_left = ((library.racer_left_finish_time - library.time_stamp_start) / 1000000000)
        time_stamp_right = ((library.racer_right_finish_time - library.time_stamp_start) / 1000000000)

        draw.rectangle([(0,100),(240,320)], fill="BLACK")
        draw.text((15,100), "Race Time Left:", fill="WHITE", font=library.Font2)
        draw.text((15,200), "Race time Right:", fill="WHITE", font=library.Font2)

        library.write_race_time(draw, library.Font2, library.time_stamp_start, time_stamp_left, library.racer_left_start_time, library.racer_left_finish_time, racer_name_left, 124)
        library.write_race_time(draw, library.Font2, library.time_stamp_start, time_stamp_right, library.racer_right_start_time, library.racer_right_finish_time, racer_name_right, 224)

        library.rotate_print(image)
        time.sleep(30)

        draw.rectangle([(0,100),(240,320)], fill="BLACK")
        draw.text((65, 100), 'END RACE', fill="WHITE", font=library.Font2)
        library.rotate_print(image)
        time.sleep(5)

        library.disp.clear()
        library.disp.module_exit()

    except KeyboardInterrupt:
        try:
            picam2_0.stop_recording()
            picam2_1.stop_recording()

            if library.racer_left_start_time != 0 and library.racer_left_finish_time == 0:
                with open("race_results.txt", "a") as file:
                    file.write(f"Left racer ({racer_name_left}): Race not finished\n")

            if library.racer_right_start_time != 0 and library.racer_right_finish_time == 0:
                with open("race_results.txt", "a") as file:
                    file.write(f"Right racer ({racer_name_right}): Race not finished\n")

            library.disp.clear()
            library.disp.module_exit()
            GPIO.cleanup()

        except Exception as e:
            print(f"Error during KeyboardInterrupt handling: {e}")
