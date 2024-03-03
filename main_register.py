from race_setup import RaceSetup
import RPi.GPIO as GPIO
import time
import threading
from PIL import Image, ImageDraw, ImageFont

# Initialize RaceSetup
race_setup = RaceSetup()

# Setup GPIO, display, camera, and threads
race_setup.setup_all()

#Set Fonts
Font1 = ImageFont.truetype("Font/Font02.ttf",30)
Font2 = ImageFont.truetype("Font/Font02.ttf",24)
Font3 = ImageFont.truetype("Font/Font02.ttf",15)
Font4 = ImageFont.truetype("Font/Font02.ttf",100)


#Intrreupts fuctions

def false_start_left(channel):
    global racer_left_start_time 
    racer_left_start_time = time.process_time_ns()

def false_start_rigth(channel):
    global racer_rigth_start_time 
    racer_rigth_start_time = time.process_time_ns()

def left_lane(channel):
    global racer_left_finish_time
    global racer_left_cross
    racer_left_finish_time = time.process_time_ns()
    racer_left_cross = True


def rigth_lane(channel):
    global racer_rigth_finish_time 
    global racer_rigth 
    racer_rigth_finish_time = time.process_time_ns()
    racer_rigth = True

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

        GPIO.output(race_setup.START_BUTTON_LED, 1)

        while True:
            # Press Button to Start Race

            if GPIO.input(race_setup.START_BUTTON) == 0:

                # Start Camera recording
                race_setup.picam2_0.start_and_record_video("left_track.mp4")
                race_setup.picam2_1.start_and_record_video("right_track.mp4")

                # Enable interrupt to start and finish lane

                GPIO.add_event_detect(race_setup.SENSOR_START_LEFT, GPIO.FALLING, callback=false_start_left, bouncetime = 10)
                GPIO.add_event_detect(race_setup.SENSOR_START_RIGHT, GPIO.FALLING, callback=false_start_rigth, bouncetime = 10)

                GPIO.add_event_detect(race_setup.SENSOR_FINISH_LEFT, GPIO.FALLING, callback=left_lane, bouncetime = 10)
                GPIO.add_event_detect(race_setup.SENSOR_FINISH_RIGHT, GPIO.FALLING, callback=rigth_lane, bouncetime = 10)


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
                race_setup.GPIO.output(race_setup.START_LIGHT, 1)

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

        # Disable finish sensor's
        FINISH_SENSORS = race_setup.SENSOR_FINISH_LEFT, race_setup.SENSOR_FINISH_RIGHT
        GPIO.cleanup(FINISH_SENSORS)

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