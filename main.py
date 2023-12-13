import time,sys
from RPi import GPIO
import smbus
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder

picam2 = Picamera2()
encoder = H264Encoder()

#Define GPIOS

#START BUTTON
START_BUTTON_LED = 16
START_BUTTON = 17

#LEFT SIDE OF TRACK
SENSOR_START_LEFT = 5
SENSOR_FINISH_LEFT = 6
START_LEFT_LED = 18

#RIGHT SIDO OF TRACK
#SENSOR_START_RIGTH = 0
#SENSOR_FINISH_RIGHT = 0
#START_RIGHT_LED = 0

# SET GPIO MODE LABEL BCM
GPIO.setmode(GPIO.BCM)


GPIO.setup(START_BUTTON_LED, GPIO.OUT)
GPIO.setup(START_BUTTON, GPIO.IN)

GPIO.setup(SENSOR_START_LEFT, GPIO.IN)
GPIO.setup(SENSOR_FINISH_LEFT, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(START_LEFT_LED, GPIO.OUT)

#Set Star button and START LED -> Off
GPIO.output(START_BUTTON_LED,0)
GPIO.output(START_LEFT_LED, 0)

#########################################
#LCD 16x2
# I2C addresses
bus = smbus.SMBus(1)
DISPLAY_TEXT_ADDR = 0x3e

# send command to display (no need for external use)    
def textCommand(cmd):
    bus.write_byte_data(DISPLAY_TEXT_ADDR,0x80,cmd)

# set display text \n for second line(or auto wrap)     
def setText(text):
    textCommand(0x01) # clear display
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)
    count = 0
    row = 0
    for c in text:
        if c == '\n' or count == START_BUTTON_LED:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))

#Update the display without erasing the display
def setText_norefresh(text):
    textCommand(0x02) # return home
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)
    count = 0
    row = 0
    while len(text) < 32: #clears the rest of the screen
        text += ' '
    for c in text:
        if c == '\n' or count == START_BUTTON_LED:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))

#Coder
if __name__=="__main__":
    
    #Start clock
    clock = 0

    #Start Message
    setText("Drag Race")
    time.sleep(2)

    # Wait for Race Car to stay on start mark 
    while (GPIO.input(SENSOR_START_LEFT) == 0):
        
        setText("Race Car:\nGo to Start Mark")
        time.sleep(0.05)

    #Start Race
    setText("Press the button to start race")
    GPIO.output(START_BUTTON_LED,1)

    while True:
        # Press Button to Start Race
        if (GPIO.input(START_BUTTON) == 0):
            
            for x in range(6):
            
                setText("Race Start in:\n{}".format(str((5-x))))
                time.sleep(1)
                
                if x == 5 : 
                    
                    GPIO.output(START_LEFT_LED, 1)
        
            #START LIGHTS ON
            break
            

    textCommand(0x01)

    # Start Camera recording 
    picam2.start_recording(encoder, "race.h264")
    
    #Start Race


    time_stamp_start = time.process_time_ns() 

    #Time work waiting for Race Car pass finish sensor 
    clock = 0
    while (GPIO.input(SENSOR_FINISH_LEFT) == 1):
        
        setText_norefresh("Time\n {} ms".format(str(clock)))
        #clock = 1+clock
        time.sleep(0.05)
        clock = time.process_time_ns() - time_stamp_start

    time_stamp_finish = time.process_time_ns()
    print(time_stamp_finish)
    # End Race
    textCommand(0x01)
    setText("Tempo final:\n {} ms".format(str(clock)))
    # Stop recodind
    picam2.stop_recording()
    time.sleep(10)
    
    time_stamp_race = (time_stamp_finish - time_stamp_start) / 1000000
    
    setText("Time measure\n {} ms".format(str(time_stamp_race)))
    time.sleep(15)
    #END RACE
    setText("End race!!!!!")    
    time.sleep(5)

    #Clear Display
    textCommand(0x01)

    #Clear GPIO settings to default 
    GPIO.cleanup()
    
    #end 
    exit()
