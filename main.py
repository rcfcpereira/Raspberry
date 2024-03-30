#main.py


#import os
#import sys
import time
import threading

import gpio_lib as RaceGPIO
import lcd_lib as RaceLCD
from PIL import Image
from picamera2 import Picamera2
from picamera2.encoders import MultiEncoder
import race_logging  # Import the race logging module

# Set Camera settings

picam2_0 = Picamera2(0)
picam2_1 = Picamera2(1)
encoder = MultiEncoder()

config_0 = picam2_0.create_video_configuration(main={"size": (640, 480), "format": "RGB888"}, controls={'FrameRate': 200})
config_1 = picam2_1.create_video_configuration(main={"size": (640, 480), "format": "RGB888"}, controls={'FrameRate': 200})

picam2_0.configure(config_0)
picam2_1.configure(config_1)

# Function to run camera recording in a thread
def run_camera(camera, filename):
    camera.start_and_record_video(filename)


if __name__ == "__main__":
    
    # Initialize GPIO, LCD, and other configurations as before...
    
    gpio_race = RaceGPIO.RaceGPIO()
    lcd_race = RaceLCD.RaceLCD()

    # Create image and draw of the display
    image, draw = lcd_race.create_image()
    # Load fonts
    fonts = lcd_race.create_fonts()

    # Start Camera Threads
    left_camera_thread = threading.Thread(target=run_camera, args=(picam2_0, "left_track_race1.mp4"))
    right_camera_thread = threading.Thread(target=run_camera, args=(picam2_1, "right_track_race1.mp4"))

    try:

        # Start clock
        clock = 0

        # Start Message
        draw.text((75, 5), 'Drag Race', fill="WHITE", font=fonts[0])
        lcd_race.rotate_print(image)

        time.sleep(1)

        # Start Race

        draw.text((55, 100), "Press the button", fill="WHITE", font=fonts[1])
        draw.text((55, 124), " to start race  ", fill="WHITE", font=fonts[1])

        lcd_race.rotate_print(image)

        time.sleep(1)

        print("Race System Ready")

        gpio_race.turn_on_start_button_led()

        print("Press the Start Button")

        while True:
            # Press Button to Start Race

            if gpio_race.get_start_button_state() == 0:

                # Start interrupt to start

                gpio_race.enable_start_interrupts()

                # Start Camera recording

                race_number = race_logging.get_next_race_number("race_log.csv")  # Get next race number
                run_camera(picam2_0, f"left_track_race{race_number}.mp4")  # Modified filename to include race number
                run_camera(picam2_1, f"right_track_race{race_number}.mp4")  # Modified filename to include race number

                # Display set to start
                draw.rectangle([(0, 100), (240, 320)], fill="BLACK")
                draw.text((60, 100), " Race Start in: ", fill="WHITE", font=fonts[1])
                lcd_race.rotate_print(image)

                for x in range(6):

                    draw.rectangle([(95, 124), (195, 224)], fill="BLACK")
                    draw.text((94, 124), "{}".format(str((5 - x))), fill="RED", font=fonts[3])
                    lcd_race.rotate_print(image)
                    time.sleep(1)

                clock = 0

                # Disable start sensor's
                gpio_race.disable_start_interrupts()
                time.sleep(0.01)

                # Start light on
                gpio_race.turn_on_start_light()
                # Start time
                time_stamp_start = time.process_time_ns()

                break

        # Enable finish sensor's
        gpio_race.enable_finish_interrupts()

        draw.rectangle([(0, 100), (240, 320)], fill="BLACK")
        draw.text((15, 100), "TIME:", fill="WHITE", font=fonts[1])
       
        while not(gpio_race.racer_left_cross and gpio_race.racer_right_cross or clock > 90):

            draw.rectangle([(20, 124), (240, 148)], fill="BLACK")
            draw.text((20, 124), "{:.3f} s".format(clock), fill="RED", font=fonts[1])
            lcd_race.rotate_print(image)
            clock = (time.process_time_ns() - time_stamp_start) / 1000000000

            time.sleep(0.01)

        # Disable finish sensor's
        gpio_race.disable_finish_interrupts()

        # Stop recording
        picam2_0.stop_recording()
        picam2_1.stop_recording()
        
        time_stamp_left = ((gpio_race.racer_left_finish_time - time_stamp_start) / 1000000000)
        time_stamp_right = ((gpio_race.racer_right_finish_time - time_stamp_start) / 1000000000)

        print(time_stamp_start)
        print(time_stamp_left)
        print(gpio_race.racer_left_finish_time)
        print(time_stamp_start)
        print(time_stamp_right)
        print(gpio_race.racer_right_finish_time)

        # Display final times 
        draw.rectangle([(0, 100), (240, 320)], fill="BLACK")

        # Left racer final time
        draw.text((15, 100), "Race Time Left:", fill="WHITE", font=fonts[1])

        # Check if the racer had a false start or exceeded the time limit
        left_status = "Not Finish"
        if gpio_race.racer_left == False and time_stamp_left > 0:
            left_status = "{:.3f} s".format(time_stamp_left)
        elif gpio_race.racer_left == True:
            left_status = "False Start"
        
        draw.text((20, 124), left_status, fill="RED", font=fonts[1])

        # Right racer final time
        draw.text((15, 200), "Race Time Right:", fill="WHITE", font=fonts[1])

        # Check if the racer had a false start or exceeded the time limit
        right_status = "Not Finish"
        if gpio_race.racer_right == False and time_stamp_right > 0:
            right_status = "{:.3f} s".format(time_stamp_right)
        elif gpio_race.racer_right == True:
            right_status = "False Start"
        
        draw.text((20, 224), right_status, fill="RED", font=fonts[1])

        # Display final times on LCD
        lcd_race.rotate_print(image)
        time.sleep(10)

        # End race    
        draw.rectangle([(0, 100), (240, 320)], fill="BLACK")
        draw.text((65, 100), 'END RACE', fill="WHITE", font=fonts[1])
        lcd_race.rotate_print(image)
        time.sleep(5)

        # Cleanup code for normal exit...
        lcd_race.cleanup_display()
        gpio_race.cleanup()

        # Writing to CSV file
        race_log_filename = "race_log.csv"
        race_number = race_logging.get_next_race_number(race_log_filename)  # Get next race number

        # Append race log to CSV file with missing information handled
        race_logging.append_race_log(race_log_filename, race_number, time_stamp_left, time_stamp_right, left_status, right_status)

    except KeyboardInterrupt:
        # Cleanup code for KeyboardInterrupt...

        print("User ended the program")
        # Close camera if running
        picam2_0.stop_recording()
        picam2_1.stop_recording()

        # Display: clear and close 
        lcd_race.cleanup_display()
        # GPIO Cleanup
        gpio_race.cleanup()
