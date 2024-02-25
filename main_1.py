import os
import sys
import time
import spidev as SPI
import smbus
import RPi.GPIO as GPIO
from picamera2 import Picamera2
from picamera2.encoders import MultiEncoder

#sys.path.append("..")
from lib import LCD_2inch4
from PIL import Image,ImageDraw,ImageFont

#Function to rotate screen and send to display
def rotate_print(self):
    im_r=self.rotate(180)
    disp.ShowImage(im_r)

# lcd gpio configuration:
RST = 27
DC = 25
BL = 24
bus = 0
device = 0

disp = LCD_2inch4.LCD_2inch4(spi=SPI.SpiDev(bus, device),spi_freq=40000000,rst=RST,dc=DC,bl=BL)
#disp = LCD_1inch3.LCD_1inch3()
# Initialize library.
disp.Init()
# Clear display.
disp.clear()
#Display DutyCycle
disp.bl_DutyCycle(100)
#Set Fonts
Font1 = ImageFont.truetype("Font/Font02.ttf",30)
Font2 = ImageFont.truetype("Font/Font02.ttf",24)
Font3 = ImageFont.truetype("Font/Font02.ttf",15)
Font4 = ImageFont.truetype("Font/Font02.ttf",100)

time.sleep(1)

# Create blank image for drawing.
# image = Image.new("RGB", (disp.width, disp.height), "BLACK")
# draw = ImageDraw.Draw(image)
# rotate_print(image)
image = Image.new("RGB", (disp.width, disp.height), "BLACK")
draw = ImageDraw.Draw(image)
rotate_print(image)

time.sleep(1)

#Set Camare settings
picam2_0 = Picamera2(0)
picam2_1 = Picamera2(1)
encoder = MultiEncoder()

config_0 = picam2_0.create_video_configuration(main = {"size" : (640,480), "format" : "RGB888"}, controls  = {'FrameRate': 200})
config_1 = picam2_1.create_video_configuration(main = {"size" : (640,480), "format" : "RGB888"}, controls  = {'FrameRate': 200})

picam2_0.configure(config_0)
picam2_1.configure(config_1)

#Define GPIOS

#START BUTTON
START_BUTTON_LED = 18
START_BUTTON = 19

#START LINE 
SENSOR_START_LEFT = 5
SENSOR_START_RIGTH = 6
START_LIGTH = 26
FALSE_START_LEFT_LED = 22
FALSE_START_RIGTH_LED = 23
#FINISH LINE
SENSOR_FINISH_LEFT = 16
SENSOR_FINISH_RIGTH = 17

# SET GPIO MODE LABEL BCM
GPIO.setmode(GPIO.BCM)

#SET ALL GPIO's
GPIO.setup(SENSOR_START_LEFT , GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(SENSOR_FINISH_LEFT, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(SENSOR_START_RIGTH , GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(SENSOR_FINISH_RIGTH, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setup(START_LIGTH, GPIO.OUT)
GPIO.setup(START_BUTTON_LED, GPIO.OUT)
GPIO.setup(START_BUTTON, GPIO.IN)
GPIO.setup(FALSE_START_LEFT_LED, GPIO.OUT)
GPIO.setup(FALSE_START_RIGTH_LED, GPIO.OUT)

#Set Start button and START LED -> Off
GPIO.output(START_BUTTON_LED,0)
#Set Start Led off
GPIO.output(START_LIGTH, 0)
#Set False Star LED's off
GPIO.output(FALSE_START_LEFT_LED, 0)
GPIO.output(FALSE_START_RIGTH_LED, 0)


#Define an interrupt handler
racer_left_start_time = 0
racer_rigth_start_time = 0
racer_left = False
racer_rigth = False
racer_left_finish_time = 0
racer_rigth_finish_time = 0
racer_left_cross = False
racer_rigth_cross = False

def false_start_left(channel):
    global racer_left_start_time 
    racer_left_start_time = time.process_time_ns()


def false_start_rigth(channel):
    global racer_rigth_start_time 
    racer_rigth_start_time = time.process_time_ns()

def left_lane(channel):

    global racer_left_finish_time
    global racer_left_cross
    racer_left_finish_time = time.process_time_ns()
    racer_left_cross = True


def rigth_lane(channel):
    global racer_rigth_finish_time 
    global racer_rigth 
    racer_rigth_finish_time = time.process_time_ns()
    racer_rigth = True

#Code
if __name__=="__main__":
    try:
        #Start clock
        clock = 0

        #Start Message
        draw.text((75, 5), 'Drag Race', fill = "WHITE",font=Font1)
        rotate_print(image)

        time.sleep(5)

        #Start Race

        draw.text((55,100), "Press the button", fill = "WHITE", font=Font2)
        draw.text((55,124), "  to start race ", fill = "WHITE", font=Font2)
        rotate_print(image)

        time.sleep(1)

        GPIO.output(START_BUTTON_LED,1)

        while True:
            # Press Button to Start Race

            if (GPIO.input(START_BUTTON) == 0 ):

                # Start Camera recording
                picam2_0.start_and_record_video("left_track.mp4")
                picam2_1.start_and_record_video("rigth_track.mp4")

                #Enable interrupt to start and finish lane
                GPIO.add_event_detect(SENSOR_START_LEFT, GPIO.FALLING, callback=false_start_left, bouncetime = 10)
                GPIO.add_event_detect(SENSOR_START_RIGTH, GPIO.FALLING, callback=false_start_rigth, bouncetime = 10)

                GPIO.add_event_detect(SENSOR_FINISH_LEFT, GPIO.FALLING, callback=left_lane, bouncetime = 10)
                GPIO.add_event_detect(SENSOR_FINISH_RIGTH, GPIO.FALLING, callback=rigth_lane, bouncetime = 10)

                #Display set to start
                draw.rectangle([(0,100),(240,320)],fill = "BLACK")
                draw.text((60,100), " Race Start in: ", fill = "WHITE", font=Font2)
                rotate_print(image)

                for x in range(6):
                    
                    draw.rectangle([(95,124),(195,224)],fill = "BLACK")
                    draw.text((94,124), "{}".format(str((5-x))), fill = "RED", font = Font4)
                    rotate_print(image)
                    time.sleep(1)

                    if racer_left_start_time != 0:
                        GPIO.output(FALSE_START_LEFT_LED, 1)
                    if racer_rigth_start_time != 0:                 
                        GPIO.output(FALSE_START_RIGTH_LED, 1)
                    
                clock = 0
                time_stamp_start = time.process_time_ns()
                GPIO.output(START_LIGTH, 1)
            
                break
             
        draw.rectangle([(0,100),(240,320)],fill = "BLACK")
        draw.text((15,100), "TIME:", fill = "WHITE", font=Font2)
    
        #Disable start sensor's
        START_SENSORS = SENSOR_START_LEFT, SENSOR_START_RIGTH
        GPIO.cleanup(START_SENSORS)

        while (racer_left!=True and racer_rigth!=True):
            
            draw.rectangle([(20,124),(240,148)],fill = "BLACK")
            draw.text((20,124), "{:.3f} s".format(clock), fill = "RED", font = Font2)
            rotate_print(image)
            clock = (time.process_time_ns() - time_stamp_start) / 1000000000
            
            time.sleep(0.01)

        #time_stamp_finish = time.process_time_ns()
        #print(time_stamp_finish)

        # Stop recodind
        picam2_0.stop_recording()
        picam2_1.stop_recording()
        
        # print(time_stamp_start)
        #print(time_stamp_finish)

        time_stamp_left = ((racer_left_finish_time - time_stamp_start) / 1000000000)
        time_stamp_rigth = ((racer_rigth_finish_time - time_stamp_start) / 1000000000)

        draw.rectangle([(0,100),(240,320)],fill = "BLACK")
        draw.text((15,100), "Race Time Left:", fill = "WHITE", font=Font2)
        draw.text((15,200), "Race time Rigth:", fill = "WHITE", font=Font2)

        if racer_left_start_time == 0:        
            draw.text((20,124), "{:.3f} s".format(time_stamp_left), fill = "RED", font = Font2)
        else:
            draw.text((20,124), "False Start", fill = "RED", font = Font2)
        if racer_rigth_start_time == 0:
            draw.text((20,224), "{:.3f} s".format(time_stamp_rigth), fill = "RED", font = Font2)
        else:
            draw.text((20,224), "False Start", fill = "RED", font = Font2)

        rotate_print(image)
        time.sleep(30)

        draw.rectangle([(0,100),(240,320)],fill = "BLACK")
        draw.text((65, 100), 'END RACE', fill = "WHITE",font=Font2)
        rotate_print(image)
        time.sleep(5)

        # print(time_stamp_start)
        # print(racer_left_start_time)
        # print(racer_rigth_start_time)
        # #print(time_stamp_finish)
        # print(racer_left_finish_time)
        # print(((racer_left_finish_time-time_stamp_start)/1000000000))
        # print(racer_rigth_finish_time)
        # print(((racer_rigth_finish_time-time_stamp_start)/1000000000))
        
        disp.clear()
        disp.module_exit()

        GPIO.cleanup()
        
    # Handle KeyboardInterrupt (Ctrl+C) to cleanup GPIO, close display, and disable cameras 
    except KeyboardInterrupt:
        
        print("end:1")
        # close camera if running
        picam2_0.stop_recording()
        picam2_1.stop_recording()
        #Display: clear and close 
        disp.clear()
        disp.module_exit()
        #GPIO Cleanup
        GPIO.cleanup()