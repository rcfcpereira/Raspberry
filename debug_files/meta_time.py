import RPi.GPIO as GPIO
import time 

#START LINE 
SENSOR_START_LEFT = 5
SENSOR_START_RIGTH = 6
START_LIGTH = 26
FALSE_START_LEFT_LED = 22
FALSE_START_RIGTH_LED = 23

#FINISH LINE
SENSOR_FINISH_LEFT = 16
SENSOR_FINISH_RIGTH = 17

GPIO.cleanup()

GPIO.setmode(GPIO.BCM)

GPIO.setup(SENSOR_START_LEFT , GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(SENSOR_FINISH_LEFT, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(SENSOR_START_RIGTH , GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(SENSOR_FINISH_RIGTH, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setup(START_LIGTH, GPIO.OUT)
GPIO.setup(FALSE_START_LEFT_LED, GPIO.OUT)
GPIO.setup(FALSE_START_RIGTH_LED, GPIO.OUT)

GPIO.output(START_LIGTH, 0)
GPIO.output(FALSE_START_LEFT_LED, 0)
GPIO.output(FALSE_START_RIGTH_LED, 0)


#Define an interrupt handler
racer_left_start_time = 0
racer_rigth_start_time = 0
racer_left = False
racer_rigth = False
racer_left_finish_time = 0
racer_rigth_finish_time = 0
racer_left_cross = False
racer_rigth_cross = False


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



GPIO.add_event_detect(SENSOR_START_LEFT, GPIO.FALLING, callback=false_start_left, bouncetime = 10) #bouncetime=100
GPIO.add_event_detect(SENSOR_START_RIGTH, GPIO.FALLING, callback=false_start_rigth, bouncetime = 10)

GPIO.add_event_detect(SENSOR_FINISH_LEFT, GPIO.FALLING, callback=left_lane, bouncetime = 10) #bouncetime=100
GPIO.add_event_detect(SENSOR_FINISH_RIGTH, GPIO.FALLING, callback=rigth_lane, bouncetime = 10)



for x in range(6):
    time.sleep(1)
    print((5-x))

    if racer_left_start_time != 0:
         GPIO.output(FALSE_START_LEFT_LED, 1)
    if racer_rigth_start_time != 0:
         GPIO.output(FALSE_START_RIGTH_LED, 1)


#Start race timer
clock = 0
time_stamp_start = time.process_time_ns()
GPIO.output(START_LIGTH, 1)

#Disable start sensor's
START_SENSORS = SENSOR_START_LEFT, SENSOR_START_RIGTH
time.sleep(0.5)
GPIO.cleanup(START_SENSORS)


while (racer_left!=True and racer_rigth!=True):

        # clock = (time.process_time_ns() - time_stamp_start) / 1000000000
        # time.sleep(0.01)

        if racer_left_cross == True: 
            racer_left_finish_time = time.process_time_ns()
            racer_left = True
        if racer_rigth_cross == True:
            racer_rigth_finish_time = time.process_time_ns()
            racer_rigth = True

time.sleep(1)

time_stamp_finish = time.process_time_ns()
race_total_time = (time_stamp_finish - time_stamp_start )/ 1000000000

print(time_stamp_start)
print(racer_left_start_time)
print(racer_rigth_start_time)
print(time_stamp_finish)
print(race_total_time)
print(racer_left_finish_time)
print(((racer_left_finish_time-time_stamp_start)/1000000000))
print(racer_rigth_finish_time)
print(((racer_rigth_finish_time-time_stamp_start)/1000000000))

GPIO.cleanup()
