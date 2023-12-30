
import os
import sys 
import time
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch54
from lib import LCD_1inch3
from PIL import Image,ImageDraw,ImageFont
from RPi import GPIO
import smbus
from picamera2 import Picamera2
from picamera2.encoders import MultiEncoder

#Function to rotate screen and send to display
def rotate_print(self):
    im_r=self.rotate(270)
    disp.ShowImage(im_r)

# lcd gpio configuration:
RST = 27
DC = 25
BL = 15
bus = 0 
device = 0 

disp = LCD_1inch3.LCD_1inch3(spi=SPI.SpiDev(bus, device),spi_freq=100000000,rst=RST,dc=DC,bl=BL)
#disp = LCD_1inch3.LCD_1inch3()
# Initialize library.
disp.Init()
# Clear display.
disp.clear()

#Set Fonts
Font1 = ImageFont.truetype("Font/Font02.ttf",40)
Font2 = ImageFont.truetype("Font/Font02.ttf",35)
Font3 = ImageFont.truetype("Font/Font02.ttf",20)

# Create blank image for drawing.
image = Image.new("RGB", (disp.width, disp.height), "BLACK")
draw = ImageDraw.Draw(image)
disp.ShowImage(image)

#Set Camare settings
picam2_0 = Picamera2(0)
picam2_1 = Picamera2(1)
encoder = MultiEncoder()

config_0 = picam2_0.create_video_configuration(main = {"size" : (640,480), "format" : "RGB888"}, controls  = {'FrameRate': 120})
config_1 = picam2_1.create_video_configuration(main = {"size" : (640,480), "format" : "RGB888"}, controls  = {'FrameRate': 120})

picam2_0.configure(config_0)
picam2_1.configure(config_1)


#Define GPIOS

#START BUTTON
START_BUTTON_LED = 16
START_BUTTON = 17

#LEFT SIDE OF TRACK
SENSOR_START_LEFT = 5
SENSOR_FINISH_LEFT = 6
START_LEFT_LED = 18
START_LINE_CHECK = 19

#RIGHT SIDO OF TRACK
#SENSOR_START_RIGTH = 0
#SENSOR_FINISH_RIGHT = 0
#START_RIGHT_LED = 0

# SET GPIO MODE LABEL BCM
GPIO.setmode(GPIO.BCM)

GPIO.setup(START_BUTTON_LED, GPIO.OUT)
GPIO.setup(START_BUTTON, GPIO.IN)

GPIO.setup(SENSOR_START_LEFT, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(SENSOR_FINISH_LEFT, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(START_LEFT_LED, GPIO.OUT)
GPIO.setup(START_LINE_CHECK, GPIO.OUT)

#Set Start button and START LED -> Off
GPIO.output(START_BUTTON_LED,0)
#Set Start Led off
GPIO.output(START_LEFT_LED, 0)
#Set Start Line check on
GPIO.output(START_LINE_CHECK, 1)


# Define an interrupt handler
class events:
    @staticmethod
    def line_checker():
        
        if (GPIO.input(SENSOR_START_LEFT) == 1):

            GPIO.output(START_LINE_CHECK,1)
            print("Void")

        else:
            
            GPIO.output(START_LINE_CHECK,0)
            print("READY")

# Attach the interrupt handler to GPIO23 with a rising-edge trigger
GPIO.add_event_detect(SENSOR_START_LEFT, GPIO.BOTH, events.line_checker(), bouncetime = 500) #bouncetime=100

# #########################################
# #LCD 16x2
# # I2C addresses
# bus = smbus.SMBus(1)
# DISPLAY_TEXT_ADDR = 0x3e

# # send command to display (no need for external use)    
# def textCommand(cmd):
#     bus.write_byte_data(DISPLAY_TEXT_ADDR,0x80,cmd)

# # set display text \n for second line(or auto wrap)     
# def setText(text):
#     textCommand(0x01) # clear display
#     time.sleep(.05)
#     textCommand(0x08 | 0x04) # display on, no cursor
#     textCommand(0x28) # 2 lines
#     time.sleep(.05)
#     count = 0
#     row = 0
#     for c in text:
#         if c == '\n' or count == 16:
#             count = 0
#             row += 1
#             if row == 2:
#                 break
#             textCommand(0xc0)
#             if c == '\n':
#                 continue
#         count += 1
#         bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))

# #Update the display without erasing the display
# def setText_norefresh(text):
#     textCommand(0x02) # return home
#     time.sleep(.05)
#     textCommand(0x08 | 0x04) # display on, no cursor
#     textCommand(0x28) # 2 lines
#     time.sleep(.05)
#     count = 0
#     row = 0
#     while len(text) < 32: #clears the rest of the screen
#         text += ' '
#     for c in text:
#         if c == '\n' or count == 16:
#             count = 0
#             row += 1
#             if row == 2:
#                 break
#             textCommand(0xc0)
#             if c == '\n':
#                 continue
#         count += 1
#         bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))

#Coder
if __name__=="__main__":

    #Start clock
    clock = 0

    #Start Message
    # setText("Drag Race")
    draw.text((10, 5), 'Drag Race', fill = "WHITE",font=Font1)
    im_r=image.rotate(270)
    disp.ShowImage(im_r)
    
    time.sleep(10)

    # Wait for Race Car to stay on start mark
    # while (GPIO.input(SENSOR_START_LEFT) == 0):

    #     setText("Race Car:\nGo to Start Mark")
    #     time.sleep(0.05)

    #Start Race
    # setText("Press the button to start race")
    draw.rectangle([(9,240),(240,240)],fill = "BLACK")
    draw.text((5,40), "Press the button", fill = "WHITE", font=Font2)
    draw.text((5,80), "  to start race ", fill = "WHITE", font=Font2)
    rotate_print(image)

    GPIO.output(START_BUTTON_LED,1)

    

    while True:
        # Press Button to Start Race
        
        if (GPIO.input(START_BUTTON) == 0 and GPIO.input(SENSOR_START_LEFT) == 1):

            # Start Camera recording 
            picam2_0.start_and_record_video("left_track.mp4")
            picam2_1.start_and_record_video("rigth_track.mp4")

            draw.rectangle([(9,240),(240,240)],fill = "BLACK")
            draw.text((5,40), "Race Start in:", fill = "WHITE", font=Font2)
            rotate_print(image)

            for x in range(6):

                # setText("Race Start in:\n{}".format(str((5-x))))
                # time.sleep(1)
                draw.rectangle([(9,75),(40,115)],fill = "BLACK")
                draw.text((10,75), "{}".format(str((5-x))), fill = "RED", font = Font1)
                rotate_print(image)
                time.sleep(1)

                if x == 5 : 
                    #START LIGHTS ON
                    GPIO.output(START_LEFT_LED, 1)
           
                    break

                #textCommand(0x01)

                # Start Camera recording 
                # picam2_0.start_and_record_video("race_0.mp4")
                # picam2_1.start_and_record_video("race_1.mp4")
                
                #Start Race

    time_stamp_start = time.process_time_ns() 

    #Time work waiting for Race Car pass finish sensor 
    clock = 0
    while (GPIO.input(SENSOR_FINISH_LEFT) == 1):
        
        # setText_norefresh("Time\n {} ms".format(str(clock)))
        #clock = 1+clock
        time.sleep(0.05)
        clock = time.process_time_ns() - time_stamp_start

    time_stamp_finish = time.process_time_ns()
    print(time_stamp_finish)
    # End Race
    # textCommand(0x01)
    # setText("Tempo final:\n {} ms".format(str(clock)))
    
    # Stop recodind
    picam2_0.stop_recording()
    picam2_1.stop_recording()
    time.sleep(10)
    
    time_stamp_race = (time_stamp_finish - time_stamp_start) / 1000000
    
    # setText("Time measure\n {} ms".format(str(time_stamp_race)))
    # time.sleep(15)
    # #END RACE
    # setText("End race!!!!!")    
    # time.sleep(5)

    # #Clear Display
    # textCommand(0x01)

    #Clear GPIO settings to default
    # p.stop()
    GPIO.cleanup()
    disp.module_exit()
    
    #end 
    exit()
