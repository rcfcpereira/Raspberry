from RPi import GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT)

if __name__ == "__main__":
    try:
        while 1:
            GPIO.output(18,0)

            sleep(0.5)

            GPIO.output(18,1)

            sleep(0.5)

    except KeyboardInterrupt:
        
        GPIO.cleanup()

