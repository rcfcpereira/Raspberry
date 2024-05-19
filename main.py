#main.py

# Import the necessary libraries
import time
import threading
from picamera2 import Picamera2
from picamera2.encoders import MultiEncoder

# Import the custom libraries
import gpio_lib as RaceGPIO
import lcd_lib as RaceLCD
import race_logging  # Import the race logging module

# Set Camera settings

picam2_0 = Picamera2(0)
picam2_1 = Picamera2(1)
encoder = MultiEncoder()

config_0 = picam2_0.create_video_configuration(main={"size": (640, 480), "format": "RGB888"}, controls={'FrameRate': 250})
config_1 = picam2_1.create_video_configuration(main={"size": (640, 480), "format": "RGB888"}, controls={'FrameRate': 250})

picam2_0.configure(config_0)
picam2_1.configure(config_1)

# Function to run camera recording in a thread
def run_camera(camera, filename):
    camera.start_and_record_video(filename)

# Main function
if __name__ == "__main__":
    
    # Initialize GPIO, LCD, and other configurations as before...
    
    gpio_race = RaceGPIO.RaceGPIO()
    lcd_race = RaceLCD.RaceLCD()
    race_logging.initialize_race_log("race_log.csv")

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

    # Start Message on LCD
        draw.text((55, 100), "Press the button", fill="WHITE", font=fonts[1])
        draw.text((55, 124), " to start race  ", fill="WHITE", font=fonts[1])
        lcd_race.rotate_print(image)

        time.sleep(1)

      # Start Message on console
        print("\nRace System Ready\n")

        # Turn on start button LED
        gpio_race.turn_on_start_button_led()
        
        print("\nPress the Start Button\n")

    # Wait for the start button to be pressed
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

                # Countdown to start
                for x in range(6):

                    draw.rectangle([(95, 124), (195, 224)], fill="BLACK")
                    draw.text((94, 124), "{}".format(str((5 - x))), fill="RED", font=fonts[3])
                    lcd_race.rotate_print(image)
                    time.sleep(1)

                #reset clock

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

        # Display set to time counting
        draw.rectangle([(0, 100), (240, 320)], fill="BLACK")
        draw.text((15, 100), "TIME:", fill="WHITE", font=fonts[1])
       
       # Time counting, until both racers cross the finish line or time exeeds x seconds
        while not(gpio_race.racer_left_cross and gpio_race.racer_right_cross or clock > 5):

            draw.rectangle([(20, 124), (240, 148)], fill="BLACK")
            draw.text((20, 124), "{:.3f} s".format(clock), fill="RED", font=fonts[1])
            lcd_race.rotate_print(image)
            clock = (time.process_time_ns() - time_stamp_start) / 1000000000

            time.sleep(0.01)

        # Disable finish sensor's
        gpio_race.disable_finish_interrupts()

        # Stop recording camera
        picam2_0.stop_recording()
        picam2_1.stop_recording()
        
        # Calculate final times
        time_stamp_left = ((gpio_race.racer_left_finish_time - time_stamp_start) / 1000000000)
        time_stamp_right = ((gpio_race.racer_right_finish_time - time_stamp_start) / 1000000000)
   
        # Check if the racer had a false start or exceeded the time limit
        left_status = "Finish"
        if gpio_race.racer_left == False and time_stamp_left < 0:
            left_status = "Not Finish"
        elif gpio_race.racer_left == True:
            left_status = "False Start"
                
        # Check if the racer had a false start or exceeded the time limit
        right_status = "Finish"
        if gpio_race.racer_right == False and time_stamp_right < 0:
            right_status = "Not Finish"
        elif gpio_race.racer_right == True:
            right_status = "False Start"

        # Print final times on console
        print("Left Racer:")
        print("Time: {:.3f}  Status: {}\n".format(time_stamp_left, left_status))
        print("Right Racer Time:")
        print("Time: {:.3f}  Status: {}\n".format(time_stamp_right, right_status))

        # Display final times 
        draw.rectangle([(0, 100), (240, 320)], fill="BLACK")

        # Left racer final time
        draw.text((15, 100), "Race Time Left:", fill="WHITE", font=fonts[1])
        if left_status == "Finish":
            draw.text((20, 124), "{:.3f} s".format(time_stamp_left), fill="RED", font=fonts[1])
        else:
            draw.text((20, 124), left_status, fill="RED", font=fonts[1])

        # Right racer final time
        draw.text((15, 200), "Race Time Right:", fill="WHITE", font=fonts[1])        
        if right_status == "Finish":
            draw.text((20, 224), "{:.3f} s".format(time_stamp_right), fill="RED", font=fonts[1])
        else:  
            draw.text((20, 224), right_status, fill="RED", font=fonts[1])

        # Display final times on LCD
        lcd_race.rotate_print(image)
        time.sleep(5)

        # End race message
        draw.rectangle([(0, 100), (240, 320)], fill="BLACK")
        draw.text((65, 100), 'END RACE', fill="WHITE", font=fonts[1])
        lcd_race.rotate_print(image)
        time.sleep(5)

        # Cleanup gpio and lcd for normal exit...
        lcd_race.cleanup_display()
        gpio_race.cleanup()

        # Writing to CSV file
        race_log_filename = "race_log.csv"
        race_number = race_logging.get_next_race_number(race_log_filename)  # Get next race number

        # Append race log to CSV file with missing information handled
        race_logging.append_race_log(race_log_filename, race_number, time_stamp_left, time_stamp_right, left_status, right_status)

        #End message on console
        print("\nRace Ended\n")

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
