# gpio_lib.py

import RPi.GPIO as GPIO
import time

class RaceGPIO:
    def __init__(self):
        """
        Initialize the RaceGPIO class.

        Args:
            None

        Returns:
            None
        """
        # Constants for pin numbers
        self.START_BUTTON_LED = 18
        self.START_BUTTON = 19
        self.SENSOR_START_LEFT = 5
        self.SENSOR_START_RIGHT = 6
        self.START_LIGHT = 26
        self.FALSE_START_LEFT_LED = 22
        self.FALSE_START_RIGHT_LED = 23
        self.SENSOR_FINISH_LEFT = 16
        self.SENSOR_FINISH_RIGHT = 17

        # Set GPIO mode to BCM
        GPIO.setmode(GPIO.BCM)

        # Set up GPIO pins
        GPIO.setup(self.SENSOR_START_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.SENSOR_FINISH_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.SENSOR_START_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.SENSOR_FINISH_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.START_LIGHT, GPIO.OUT)
        GPIO.setup(self.START_BUTTON_LED, GPIO.OUT)
        GPIO.setup(self.START_BUTTON, GPIO.IN)
        GPIO.setup(self.FALSE_START_LEFT_LED, GPIO.OUT)
        GPIO.setup(self.FALSE_START_RIGHT_LED, GPIO.OUT)

        # Initialize state variables
        self.racer_left = False
        self.racer_right = False
        self.racer_left_finish_time = 0
        self.racer_right_finish_time = 0
        self.racer_left_cross = False
        self.racer_right_cross = False

    # Interrupt Handlers in the class
    def false_start_left(self, channel):
        """
        Handler for false start event in the left lane.

        Args:
            channel (int): GPIO channel number.

        Returns:
            None
        """
        if self.racer_left == False:
            self.racer_left = True
            self.turn_on_false_start_left_led()

    def false_start_right(self, channel):
        """
        Handler for false start event in the right lane.

        Args:
            channel (int): GPIO channel number.

        Returns:
            None
        """
        if self.racer_right == False:
            self.racer_right = True
            self.turn_on_false_start_right_led()

    def finish_left_lane(self, channel):
        """
        Handler for finish event in the left lane.

        Args:
            channel (int): GPIO channel number.

        Returns:
            None
        """
        if self.racer_left_cross == False:
            self.racer_left_finish_time = time.process_time_ns()
            self.racer_left_cross = True
            print("Left lane finish\n")

    def finish_right_lane(self, channel):
        """
        Handler for finish event in the right lane.

        Args:
            channel (int): GPIO channel number.

        Returns:
            None
        """
        if self.racer_right_cross == False:
            self.racer_right_finish_time = time.process_time_ns()
            self.racer_right_cross = True
            print("Right lane finish\n")

    def turn_on_start_light(self):
        """
        Turn on the start light.

        Args:
            None

        Returns:
            None
        """
        GPIO.output(self.START_LIGHT, 1)
        print("Start light on\n")

    def turn_on_start_button_led(self):
        """
        Turn on the start button LED.

        Args:
            None

        Returns:
            None
        """
        GPIO.output(self.START_BUTTON_LED, 1)

    def turn_on_false_start_left_led(self):
        """
        Turn on the false start LED in the left lane.

        Args:
            None

        Returns:
            None
        """
        GPIO.output(self.FALSE_START_LEFT_LED, 1)
        print("\nFalse start left\n")

    def turn_on_false_start_right_led(self):
        """
        Turn on the false start LED in the right lane.

        Args:
            None

        Returns:
            None
        """
        GPIO.output(self.FALSE_START_RIGHT_LED, 1)
        print("\nFalse start right\n")

    def get_start_button_state(self):
        """
        Get the state of the start button.

        Args:
            None

        Returns:
            int: State of the start button (1 for pressed, 0 for not pressed).
        """
        return GPIO.input(self.START_BUTTON)

    def disable_pins(self, pins):
        """
        Clean up and disable GPIO pins.

        Args:
            pins (int or list of ints): GPIO pin numbers to clean up.

        Returns:
            None
        """
        GPIO.cleanup(pins)

    # Set interrupt handlers
    def enable_start_interrupts(self):
        """
        Enable interrupts for the start sensors.

        Args:
            None

        Returns:
            None
        """
        GPIO.add_event_detect(self.SENSOR_START_LEFT, GPIO.FALLING, callback=self.false_start_left, bouncetime=1)
        GPIO.add_event_detect(self.SENSOR_START_RIGHT, GPIO.FALLING, callback=self.false_start_right, bouncetime=1)

    def enable_finish_interrupts(self):
        """
        Enable interrupts for the finish sensors.

        Args:
            None

        Returns:
            None
        """
        GPIO.add_event_detect(self.SENSOR_FINISH_LEFT, GPIO.FALLING, callback=self.finish_left_lane, bouncetime=1)
        GPIO.add_event_detect(self.SENSOR_FINISH_RIGHT, GPIO.FALLING, callback=self.finish_right_lane, bouncetime=1)

    def disable_start_interrupts(self):
        """
        Disable interrupts for the start sensors.

        Args:
            None

        Returns:
            None
        """
        GPIO.remove_event_detect(self.SENSOR_START_LEFT)
        GPIO.remove_event_detect(self.SENSOR_START_RIGHT)

    def disable_finish_interrupts(self):
        """
        Disable interrupts for the finish sensors.

        Args:
            None

        Returns:
            None
        """
        GPIO.remove_event_detect(self.SENSOR_FINISH_LEFT)
        GPIO.remove_event_detect(self.SENSOR_FINISH_RIGHT)

    #clean up GPIO's configuration for loop
    def loop_cleanup(self):
        """
        Clean up GPIO configuration and variables.

        Args:
            None

        Returns:
            None
        """
        GPIO.output(self.START_LIGHT, 0)
        GPIO.output(self.START_BUTTON_LED, 0)
        GPIO.output(self.FALSE_START_LEFT_LED, 0)
        GPIO.output(self.FALSE_START_RIGHT_LED, 0)

        self.racer_left = False
        self.racer_right = False
        self.racer_left_finish_time = 0
        self.racer_right_finish_time = 0
        self.racer_left_cross = False
        self.racer_right_cross = False       

    # Cleanup GPIO's configuration pins
    def cleanup(self):
        """
        Clean up GPIO configuration.

        Args:
            None

        Returns:
            None
        """
        GPIO.cleanup()