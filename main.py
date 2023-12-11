import time,sys
from RPi import GPIO
import smbus
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder

picam2 = Picamera2(0)
encoder = H264Encoder()

#Define GPIOS

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(5, GPIO.IN)
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)
#Led Star button Off
GPIO.output(16,0)

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
        if c == '\n' or count == 16:
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
        if c == '\n' or count == 16:
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
#Wait for Race Car to stay on start mark 
    while (GPIO.input(5) == 0):
        
        setText("Race Car:\nGo to Start Mark")
        time.sleep(0.5)
#Start Race
    setText("Press the button to start race")
    GPIO.output(16,1)

    while True:
        # Press Button to Start Race
        if (GPIO.input(17) == 0):
            
            for x in range(6):
            
                setText("Race Start in:\n{}".format(str(x)))
                time.sleep(1)
        
            break
            

    textCommand(0x01)

    # Start Camera recording 
    picam2.start_recording(encoder, "race.h264")
    
    #Start Race

    #Clock work waiting for Race Car pass finish sensor 
    
    while (GPIO.input(18) == 1):
        
        setText_norefresh("Time\n {}".format(str(clock)))
        clock = 1+clock
        time.sleep(0.01)

    # End Race
    textCommand(0x01)
    setText("Tempo final:\n {}".format(str(clock)))
    # Stop recodind
    picam2.stop_recording()
    time.sleep(10)

    setText("End race!!!!!")    
    time.sleep(5)

    #Clear Display
    textCommand(0x01)
    #Clear GPIO settings to default 
    GPIO.cleanup()
    #end 
    exit()
