# gpio_lib.py

import RPi.GPIO as GPIO
import time

class RaceGPIO:
    def __init__(self):
        # Constants for pin numbers
        self.START_BUTTON_LED = 18
        self.START_BUTTON = 19
        self.SENSOR_START_LEFT = 5
        self.SENSOR_START_RIGHT = 6
        self.START_LIGHT = 26
        self.FALSE_START_LEFT_LED = 22
        self.FALSE_START_RIGHT_LED = 23
        self.SENSOR_FINISH_LEFT = 16
        self.SENSOR_FINISH_RIGTH = 17


        # Set GPIO mode to BCM
        GPIO.setmode(GPIO.BCM)

        # Set up GPIO pins
        GPIO.setup(self.SENSOR_START_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.SENSOR_FINISH_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.SENSOR_START_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.SENSOR_FINISH_RIGTH, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.START_LIGHT, GPIO.OUT)
        GPIO.setup(self.START_BUTTON_LED, GPIO.OUT)
        GPIO.setup(self.START_BUTTON, GPIO.IN)
        GPIO.setup(self.FALSE_START_LEFT_LED, GPIO.OUT)
        GPIO.setup(self.FALSE_START_RIGHT_LED, GPIO.OUT)

        # Initialize state variables

        self.racer_left = False
        self.racer_rigth = False
        self.racer_left_finish_time = 0
        self.racer_rigth_finish_time = 0
        self.racer_left_cross = False  
        self.racer_rigth_cross = False  

    #Intterupt Handlers in the class
        
    def false_start_left(self, channel):

        self.racer_left_start_time = time.process_time_ns()
        self.turn_on_false_start_left_led()

    def false_start_right(self, channel):

        self.racer_right_start_time = time.process_time_ns()
        self.turn_on_false_start_right_led()     

    def finish_left_lane(self, channel):

        self.racer_left_finish_time = time.process_time_ns()
        self.racer_left_cross = True
        print("Left lane finish")

    def finish_right_lane(self, channel):

        self.racer_rigth_finish_time = time.process_time_ns()
        self.racer_rigth_cross = True
        print("Right lane finish")

    def turn_on_start_light(self):

        GPIO.output(self.START_LIGHT, 1)

    def turn_on_start_button_led(self):

        GPIO.output(self.START_BUTTON_LED, 1)

    def turn_on_false_start_left_led(self):

        GPIO.output(self.FALSE_START_LEFT_LED, 1)

    def turn_on_false_start_right_led(self):

        GPIO.output(self.FALSE_START_RIGHT_LED, 1)

    def get_start_button_state(self):

        return GPIO.input(self.START_BUTTON)

    def disable_pins(self, pins):

        GPIO.cleanup(pins)

    # Set interrupt handlers
    def enable_start_interrupts(self):

        GPIO.add_event_detect(self.SENSOR_START_LEFT, GPIO.FALLING, callback=self.false_start_left, bouncetime=1)
        GPIO.add_event_detect(self.SENSOR_START_RIGHT, GPIO.FALLING, callback=self.false_start_right, bouncetime=1)

    def enable_finish_interrupts(self):

        GPIO.add_event_detect(self.SENSOR_FINISH_LEFT, GPIO.FALLING, callback=self.finish_left_lane, bouncetime=1)
        GPIO.add_event_detect(self.SENSOR_FINISH_RIGTH, GPIO.FALLING, callback=self.finish_right_lane, bouncetime=1)

    def disable_start_interrupts(self):

        GPIO.remove_event_detect(self.SENSOR_START_LEFT)
        GPIO.remove_event_detect(self.SENSOR_START_RIGHT)

    def disable_finish_interrupts(self):

        GPIO.remove_event_detect(self.SENSOR_FINISH_LEFT)
        GPIO.remove_event_detect(self.SENSOR_FINISH_RIGTH)

    #Cleanup GPIO's configuration pins

    def get_start_button_state(self):

        return GPIO.input(self.START_BUTTON)
    
    def disable_pins(self, pins):

        GPIO.cleanup(pins) 

    # Add other methods as needed

    def cleanup(self):

        GPIO.cleanup()
