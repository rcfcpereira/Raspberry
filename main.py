import time,sys
from RPi import GPIO
import smbus
from picamera2 import Picamera2

picam2 = Picamera2


GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(5, GPIO.IN)

GPIO.output(16,1)
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

# example code
if __name__=="__main__":
    clock = 0

    setText("Drag Race")
    time.sleep(2)

    while GPIO.input(5) == 0:
         setText("Robo Fora da linha")
         time.sleep(5)
         

    textCommand(0x01)

    while (GPIO.input(17) == 1):
        
        setText_norefresh("Time\n {}".format(str(clock)))
        clock = 0.001+clock
        time.sleep(0.001)
    
    textCommand(0x01)
    setText("Tempo final:\n {}".format(str(clock)))
    
    picam2.start_and_capture_file("image.jpg")

    time.sleep(10)

    setText("End race!!!!!")
    
    GPIO.cleanup()
    
    exit()

