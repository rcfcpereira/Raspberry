from rpi_lcd import LCD
from time import sleep

lcd = LCD()


lcd.clear()

lcd.text('Hello World!', 1)
sleep(5)
lcd.text('Raspberry Pi', 2)
sleep(5)
lcd.text('is really', 3, 'center')
sleep(5)
lcd.text('awesome', 4, 'right')

sleep(5)
