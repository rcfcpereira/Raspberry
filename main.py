#main.py

# Import the necessary modules
import time # Import the time module
import threading # Import the threading module
from picamera2 import Picamera2 # Import the Picamera2 class from the picamera2 module
from picamera2.encoders import MultiEncoder # Import the MultiEncoder class from the encoders module

# Import custom modules
import gpio_lib as RaceGPIO # Import the GPIO library
import lcd_lib as RaceLCD # Import the LCD library
import race_logging  # Import the race logging module

# Constants
MAX_CLOCK = 10 # Maximum

def configure_camera():
    """
    Configures two cameras using the Picamera2 class.

    This function creates two instances of Picamera2, each with a different camera index (0 and 1). 
    It then creates two video configurations for the two cameras. Both configurations set the video size to 640x480 pixels 
    and the format to RGB888. They also set the frame rate to 200 frames per second. 
    These configurations are then applied to the respective cameras using the configure() method.

    Args:
        None

    Returns:
        tuple: A tuple containing two configured Picamera2 instances.
    """    
    picam2_0 = Picamera2(0)
    picam2_1 = Picamera2(1)
    encoder = MultiEncoder()

    config_0 = picam2_0.create_video_configuration(main={"size": (640, 480), "format": "RGB888"}, controls={'FrameRate': 200})
    config_1 = picam2_1.create_video_configuration(main={"size": (640, 480), "format": "RGB888"}, controls={'FrameRate': 200})

    picam2_0.configure(config_0)
    picam2_1.configure(config_1)

    return picam2_0, picam2_1

def run_camera(camera, filename):
    """
    Starts recording video with the given camera.

    This function tries to start recording video with the given camera using the `start_and_record_video()` method of the `camera` object. 
    If there's an exception (an error occurs), the function catches it and prints an error message.

    Args:
        camera: An instance of a camera class.
        filename (str): The name of the file where the video will be saved.

    Returns:
        None
    """
    try:
        camera.start_and_record_video(filename)
    except Exception as e:
        print(f"Failed to start and record video: {e}")

def main():
    """
    Main function of a drag race program.

    This function initializes two cameras, GPIO and LCD, and a CSV log file. It creates an image and fonts for the LCD display, 
    and initializes two threads for running the cameras. It enters an infinite loop where it waits for the start button to be pressed. 
    Once pressed, it starts recording with both cameras and displays a countdown on the LCD. When the countdown finishes, it starts a timer 
    and waits for the finish line to be crossed or for a maximum time to be reached. Once the race is finished, it stops the cameras, 
    calculates the final times, and checks if there was a false start or if the time limit was exceeded. It then prints the final times on 
    the console and displays them on the LCD. Finally, it logs the race results in the CSV file and cleans up the GPIO and LCD.

    Args:
        None

    Returns:
        None
    """    
    #Start the main program

    #Start the camera
    picam2_0, picam2_1 = configure_camera()

    #Start the GPIO and LCD
    gpio_race = RaceGPIO.RaceGPIO()
    lcd_race = RaceLCD.RaceLCD()
    #Initialize CSV
    race_logging.initialize_race_log("race_log.csv")

    #Initializa LCD image and fonts
    image, draw = lcd_race.create_image()
    fonts = lcd_race.create_fonts()

    #Initialize the camera threads
    left_camera_thread = threading.Thread(target=run_camera, args=(picam2_0, "left_track_race1.mp4"))
    right_camera_thread = threading.Thread(target=run_camera, args=(picam2_1, "right_track_race1.mp4"))

    while True:  # This is the infinite loop
        try:

            #Reset the clock variable
            clock = 0

            gpio_race.racer_left = False
            gpio_race.racer_right = False

            #LCD Start Image
            draw.text((75, 5), 'Drag Race', fill="WHITE", font=fonts[0])
            draw.text((55, 100), "Press the button", fill="WHITE", font=fonts[1])
            draw.text((55, 124), " to start race  ", fill="WHITE", font=fonts[1])
            lcd_race.rotate_print(image)
            time.sleep(1)

            #Print to console 
            print("\nRace System Ready\n")

            #Turn on the start button LED
            gpio_race.turn_on_start_button_led()

            #Print to console
            print("\nPress the Start Button\n")

            #Start Race loop
            while True:

                #Wait for the start button to be pressed
                if gpio_race.get_start_button_state() == 0:

                    gpio_race.enable_start_interrupts()

                    #Get race number from cvs file
                    race_number = race_logging.get_next_race_number("race_log.csv")
                    
                    #Cameras Starte reconrding
                    run_camera(picam2_0, f"left_track_race{race_number}.mp4")
                    run_camera(picam2_1, f"right_track_race{race_number}.mp4")

                    #LCD Countdown
                    draw.rectangle([(0, 100), (240, 320)], fill="BLACK")
                    draw.text((60, 100), " Race Start in: ", fill="WHITE", font=fonts[1])
                    lcd_race.rotate_print(image)

                    for x in range(6):
                        draw.rectangle([(95, 124), (195, 224)], fill="BLACK")
                        draw.text((94, 124), "{}".format(str((5 - x))), fill="RED", font=fonts[3])
                        lcd_race.rotate_print(image)
                        time.sleep(1)

                    #Reset the clock
                    clock = 0

                    #Enable finish interrupts
                    gpio_race.disable_start_interrupts()
                    time.sleep(0.01)
                  
                    break

            #Turn on the start light
            gpio_race.turn_on_start_light()
            #Get time start race        
            time_stamp_start = time.process_time_ns()

            #Enable finish interrupts
            gpio_race.enable_finish_interrupts()

            #LCD Race Time
            draw.rectangle([(0, 100), (240, 320)], fill="BLACK")
            draw.text((15, 100), "TIME:", fill="WHITE", font=fonts[1])

            
            while not(gpio_race.racer_left_cross and gpio_race.racer_right_cross or clock > MAX_CLOCK):

                draw.rectangle([(20, 124), (240, 148)], fill="BLACK")
                draw.text((20, 124), "{:.3f} s".format(clock), fill="RED", font=fonts[1])
                lcd_race.rotate_print(image)
                clock = (time.process_time_ns() - time_stamp_start) / 1000000000

                time.sleep(0.01)
            
            #Disable finish interrupts
            gpio_race.disable_finish_interrupts()

            #Stop the cameras
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

            lcd_race.rotate_print(image)
            time.sleep(5)

            # End race message
            draw.rectangle([(0, 100), (240, 320)], fill="BLACK")
            draw.text((65, 100), 'END RACE', fill="WHITE", font=fonts[1])
            lcd_race.rotate_print(image)
            time.sleep(5)
        
            # lcd_race.cleanup_display()
            # gpio_race.cleanup()

            race_log_filename = "race_log.csv"
            race_number = race_logging.get_next_race_number(race_log_filename)

            race_logging.append_race_log(race_log_filename, race_number, time_stamp_left, time_stamp_right, left_status, right_status)

            #End message of race on console
            print("\nRace Ended\nPress CTRL + C to end program\n")
            
            # draw.rectangle([(0, 0), (240, 320)], fill="BLACK")
            # lcd_race.rotate_print(image)

            gpio_race.loop_cleanup()

        except KeyboardInterrupt:

            #Print to console to inform user that the program has ended
            print("User ended the program")   

            # Cleanup GPIO, LCD 
            picam2_0.stop_recording()
            picam2_1.stop_recording()           
            
            # Display: clear and close
            draw.rectangle([(0, 0), (240, 320)], fill="BLACK")
            lcd_race.rotate_print(image) 
            lcd_race.cleanup_display()
            # GPIO Cleanu
            gpio_race.cleanup()

            break  # This will break the infinite loop when a KeyboardInterrupt occurs

if __name__ == "__main__":
    main()