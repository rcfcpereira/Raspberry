from race_setup import RaceSetup
import time
import threading
from PIL import Image, ImageDraw, ImageFont

# Initialize RaceSetup
race_setup = RaceSetup()

# Setup GPIO, display, camera, and threads
race_setup.setup_all()

# Create blank image for drawing
image = Image.new("RGB", (race_setup.disp.width, race_setup.disp.height), "BLACK")
draw = ImageDraw.Draw(image)

# Main function
if __name__ == "__main__":
    try:
        #Start clock
        clock = 0

        #Start Message
        draw.text((75, 5), 'Drag Race', fill="WHITE", font=Font1)
        race_setup.rotate_print(image)

        time.sleep(5)

        #Start Race
        draw.text((55, 100), "Press the button", fill="WHITE", font=Font2)
        draw.text((55, 124), "  to start race ", fill="WHITE", font=Font2)
        race_setup.rotate_print(image)

        time.sleep(1)

        race_setup.GPIO.output(race_setup.START_BUTTON_LED, 1)

        while True:
            # Press Button to Start Race

            if race_setup.GPIO.input(race_setup.START_BUTTON) == 0:

                # Start Camera recording
                race_setup.picam2_0.start_and_record_video("left_track.mp4")
                race_setup.picam2_1.start_and_record_video("right_track.mp4")

                # Enable interrupt to start and finish lane
                race_setup.GPIO.add_event_detect(race_setup.SENSOR_START_LEFT, race_setup.GPIO.FALLING, callback=race_setup.false_start_left, bouncetime=10)
                race_setup.GPIO.add_event_detect(race_setup.SENSOR_START_RIGHT, race_setup.GPIO.FALLING, callback=race_setup.false_start_right, bouncetime=10)

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
                        race_setup.GPIO.output(race_setup.FALSE_START_LEFT_LED, 1)
                    if race_setup.racer_right_start_time != 0:
                        race_setup.GPIO.output(race_setup.FALSE_START_RIGHT_LED, 1)

                clock = 0
                time_stamp_start = time.process_time_ns()
                race_setup.GPIO.output(race_setup.START_LIGHT, 1)

                break

        draw.rectangle([(0, 100), (240, 320)], fill="BLACK")
        draw.text((15, 100), "TIME:", fill="WHITE", font=Font2)

        # Disable start sensor's
        START_SENSORS = race_setup.SENSOR_START_LEFT, race_setup.SENSOR_START_RIGHT
        race_setup.GPIO.cleanup(START_SENSORS)

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

        race_setup.GPIO.cleanup()

    except KeyboardInterrupt:
        race_setup.picam2_0.stop_recording()
        race_setup.picam2_1.stop_recording()
        race_setup.disp.clear()
        race_setup.disp.module_exit()
        race_setup.GPIO.cleanup()
