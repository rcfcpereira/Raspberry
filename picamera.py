import time
from grove.grove_4_digit_display import Grove4DigitDisplay

display = Grove4DigitDisplay(18, 13)

count = 0
while True:
    t = time.strftime("%H%M", time.localtime(time.time()))
    display.show(t)
    display.set_colon(count & 1)
    count += 1
    time.sleep(1)