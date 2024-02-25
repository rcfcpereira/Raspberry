import os
import sys
import time
import RPi.GPIO as GPIO
from race_setup import RaceSetup
from PIL import Image, ImageDraw, ImageFont
import threading

# Main function
if __name__ == "__main__":
    try:
        # Initialize race setup
        race_setup = RaceSetup()
        race_setup.setup_all()

        # Create blank image for drawing
        image = Image.new("RGB", (race_setup.disp.width, race_setup.disp.height), "BLACK")
        draw = ImageDraw.Draw(image)

        # Start Message
        Font1 = ImageFont.truetype("Font/Font02.ttf", 30)
        draw.text((75, 5), 'Drag Race', fill="WHITE", font=Font1)
        race_setup.rotate_print(image)

        time.sleep(5)

        # Start Race
        Font2 = ImageFont.truetype("Font/Font02.ttf", 24)
        draw.text((55, 100), "Press the button", fill="WHITE", font=Font2)
        draw.text((55, 124), "  to start race ", fill="WHITE", font=Font2)
        race_setup.rotate_print(image)

        time.sleep(1)

        GPIO.output(race_setup.START_BUTTON_LED, 1)

        while True:
            # Press Button to Start Race
            if GPIO.input(race_setup.START_BUTTON) == 0:
                # Start Camera recording
                race_setup.thread_left_camera = threading.Thread(target=race_setup.picam2_0.start_and_record_video, args=("left_track.mp4",))
                race_setup.thread_right_camera = threading.Thread(target=race_setup.picam2_1.start_and_record_video, args=("right_track.mp4",))
                race_setup.thread_left_camera.start()
                race_setup.thread_right_camera.start()

                # Enable interrupt to start and finish lane
                GPIO.add_event_detect(race_setup.SENSOR_START_LEFT, GPIO.FALLING, callback=race_setup.false_start_left, bouncetime=10)
                GPIO.add_event_detect(race_setup.SENSOR_START_RIGHT, GPIO.FALLING, callback=race_setup.false_start_right, bouncetime=10)

                # Display set to start
                draw.rectangle([(0, 100), (240, 320)], fill="BLACK")
                draw.text((60, 100), " Race Start in: ", fill="WHITE", font=Font2)
                race_setup.rotate_print(image)

                for x in range(6):
                    draw.rectangle([(95, 124), (195, 224)], fill="BLACK")
                    draw.text((94, 124), "{}".format(str((5 - x))), fill="RED", font=Font4)
                    race_setup.rotate_print(image)
                    time.sleep(1)

                    if race_setup.racer_left_start_time != 0:
                        GPIO.output(race_setup.FALSE_START_LEFT_LED, 1)
                    if race_setup.racer_right_start_time != 0:
                        GPIO.output(race_setup.FALSE_START_RIGHT_LED, 1)

                clock = 0
                time_stamp_start = time.process_time_ns()
                GPIO.output(race_setup.START_LIGHT, 1)

                break

        draw.rectangle([(0, 100), (240, 320)], fill="BLACK")
        draw.text((15, 100), "TIME:", fill="WHITE", font=Font2)

        # Disable start sensor's
        START_SENSORS = race_setup.SENSOR_START_LEFT, race_setup.SENSOR_START_RIGHT
        GPIO.cleanup(START_SENSORS)

        while race_setup.racer_left != True and race_setup.racer_right != True:
            draw.rectangle([(20, 124), (240, 148)], fill="BLACK")
            draw.text((20, 124), "{:.3f} s".format(clock), fill="RED", font=Font2)
            race_setup.rotate_print(image)
            clock = (time.process_time_ns() - time_stamp_start) / 1000000000
            time.sleep(0.01)

        race_setup.picam2_0.stop_recording()
        race_setup.picam2_1.stop_recording()

        time_stamp_left = ((race_setup.racer_left_finish_time - time_stamp_start) / 1000000000)
        time_stamp_right = ((race_setup.racer_right_finish_time - time_stamp_start) / 1000000000)

        draw.rectangle([(0, 100), (240, 320)], fill="BLACK")
        draw.text((15, 100), "Race Time Left:", fill="WHITE", font=Font2)
        draw.text((15, 200), "Race time Right:", fill="WHITE", font=Font2)

        if race_setup.racer_left_start_time == 0:
            draw.text((20, 124), "{:.3f} s".format(time_stamp_left), fill="RED", font=Font2)
        else:
            draw.text((20, 124), "False Start", fill="RED", font=Font2)
        if race_setup.racer_right_start_time == 0:
            draw.text((20, 224), "{:.3f} s".format(time_stamp_right), fill="RED", font=Font2)
        else:
            draw.text((20, 224), "False Start", fill="RED", font=Font2)

        race_setup.rotate_print(image)
        time.sleep(30)

        draw.rectangle([(0, 100), (240, 320)], fill="BLACK")
        draw.text((65, 100), 'END RACE', fill="WHITE", font=Font2)
        race_setup.rotate_print(image)
        time.sleep(5)

        race_setup.disp.clear()
        race_setup.disp.module_exit()

        GPIO.cleanup()

    except KeyboardInterrupt:
        race_setup.picam2_0.stop_recording()
        race_setup.picam2_1.stop_recording()
        race_setup.disp.clear()
        race_setup.disp.module_exit()
        GPIO.cleanup()
