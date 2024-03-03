# main.py

import os
import sys
import time
import threading

import gpio_lib as RaceGPIO
from PIL import Image, ImageDraw, ImageFont
from picamera2 import Picamera2
from picamera2.encoders import MultiEncoder
import spidev as SPI
import smbus
from lib import LCD_2inch4

def rotate_print(self):
    im_r=self.rotate(180)
    disp.ShowImage(im_r)

# lcd gpio configuration:
RST_PIN = 27
DC_PIN = 25
BL_PIN = 24
BUS = 0
DEVICE = 0

disp = LCD_2inch4.LCD_2inch4(spi=SPI.SpiDev(BUS, DEVICE), spi_freq=40000000, rst=RST_PIN, dc=DC_PIN, bl=BL_PIN)

# Initialize library.
disp.Init()
# Clear display.
disp.clear()

# Display DutyCycle
disp.bl_DutyCycle(60)
# Set Fonts
Font1 = ImageFont.truetype("Font/Font02.ttf", 30)
Font2 = ImageFont.truetype("Font/Font02.ttf", 24)
Font3 = ImageFont.truetype("Font/Font02.ttf", 15)
Font4 = ImageFont.truetype("Font/Font02.ttf", 100)

# Create blank image for drawing.
image = Image.new("RGB", (disp.width, disp.height), "BLACK")
draw = ImageDraw.Draw(image)
rotate_print(image)

time.sleep(1)

#Set Camare settings

picam2_0 = Picamera2(0)
picam2_1 = Picamera2(1)
encoder = MultiEncoder()

config_0 = picam2_0.create_video_configuration(main={"size": (640, 480), "format": "RGB888"},controls={'FrameRate': 120})
config_1 = picam2_1.create_video_configuration(main={"size": (640, 480), "format": "RGB888"},controls={'FrameRate': 120})

picam2_0.configure(config_0)
picam2_1.configure(config_1)

# Function to run camera recording in a thread
def run_camera(camera, filename):
    camera.start_and_record_video(filename)


if __name__ == "__main__":
    # Initialize GPIO, LCD, and other configurations as before...
    
    gpio_race = RaceGPIO.RaceGPIO()

    # Start Camera Threads
    left_camera_thread = threading.Thread(target=run_camera, args=(picam2_0, "left_track.mp4"))
    right_camera_thread = threading.Thread(target=run_camera, args=(picam2_1, "right_track.mp4"))

    try:

        # Start clock
        clock = 0

        # Start Message
        draw.text((75, 5), 'Drag Race', fill="WHITE", font=Font1)
        rotate_print(image)

        time.sleep(1)

        # Start Race

        draw.text((55, 100), "Press the button", fill="WHITE", font=Font2)
        draw.text((55, 124), "  to start race ", fill="WHITE", font=Font2)

        rotate_print(image)

        time.sleep(1)

        print("Race System Ready")

        gpio_race.turn_on_start_button_led()

        print("Press the Start Button")

        while True:
            # Press Button to Start Race

            if gpio_race.get_start_button_state() == 0:

                #Start interrupt to start

                gpio_race.enable_start_interrupts()

                # Start Camera recording

                run_camera(picam2_0, "left_track.mp4")
                run_camera(picam2_1, "rigth_track.mp4")

                # Display set to start
                draw.rectangle([(0, 100), (240, 320)], fill="BLACK")
                draw.text((60, 100), " Race Start in: ", fill="WHITE", font=Font2)
                rotate_print(image)

                for x in range(6):

                    draw.rectangle([(95, 124), (195, 224)], fill="BLACK")
                    draw.text((94, 124), "{}".format(str((5 - x))), fill="RED", font=Font4)
                    rotate_print(image)
                    time.sleep(1)

                clock = 0

                # Disable start sensor's
                gpio_race.disable_start_interrupts()
                time.sleep(0.01)

                #start light on
                gpio_race.turn_on_start_light()
                #start time
                time_stamp_start = time.process_time_ns()

                break

        # Enable finish sensor's
        gpio_race.enable_finish_interrupts()

        draw.rectangle([(0, 100), (240, 320)], fill="BLACK")
        draw.text((15, 100), "TIME:", fill="WHITE", font=Font2)
       
        while not(gpio_race.racer_left_cross and gpio_race.racer_rigth_cross):

            draw.rectangle([(20, 124), (240, 148)], fill="BLACK")
            draw.text((20, 124), "{:.3f} s".format(clock), fill="RED", font=Font2)
            rotate_print(image)
            clock = (time.process_time_ns() - time_stamp_start) / 1000000000

            time.sleep(0.01)

        # Disable finish sensor's
        gpio_race.disable_finish_interrupts()

        # Stop recording
        picam2_0.stop_recording()
        picam2_1.stop_recording()
        
        time_stamp_left = ((gpio_race.racer_left_finish_time - time_stamp_start) / 1000000000)
        time_stamp_rigth = ((gpio_race.racer_rigth_finish_time - time_stamp_start) / 1000000000)

        print(time_stamp_start)
        print(time_stamp_left)
        print(gpio_race.racer_left_finish_time)
        print(time_stamp_start)
        print(time_stamp_rigth)
        print(gpio_race.racer_rigth_finish_time )


        draw.rectangle([(0, 100), (240, 320)], fill="BLACK")
        draw.text((15, 100), "Race Time Left:", fill="WHITE", font=Font2)
        if gpio_race.racer_left == False:
            draw.text((20, 124), "{:.3f} s".format(time_stamp_left), fill="RED", font=Font2)
        else:
            draw.text((20, 124), "False Start", fill="RED", font=Font2)
        draw.text((15, 200), "Race time Rigth:", fill="WHITE", font=Font2)
        if gpio_race.racer_rigth == False:
            draw.text((20, 224), "{:.3f} s".format(time_stamp_rigth), fill="RED", font=Font2)
        else:
            draw.text((20, 224), "False Start", fill="RED", font=Font2)

        rotate_print(image)
        time.sleep(30)

        draw.rectangle([(0, 100), (240, 320)], fill="BLACK")
        draw.text((65, 100), 'END RACE', fill="WHITE", font=Font2)
        rotate_print(image)
        time.sleep(5)

        disp.clear()
        disp.module_exit()

        gpio_race.cleanup()

    except KeyboardInterrupt:
        # Cleanup code for KeyboardInterrupt...

        print("User ended the program")
        # close camera if running
        picam2_0.stop_recording()
        picam2_1.stop_recording()

        #Display: clear and close 
        disp.clear()
        disp.module_exit()
        #GPIO Cleanup

        gpio_race.cleanup()