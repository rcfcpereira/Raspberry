# # #!/usr/bin/python
# # # -*- coding: UTF-8 -*-
# import os
# import sys 
# import time
# import spidev as SPI
# #sys.path.append("..")
# #from lib import LCD_1inch54
# from lib import LCD_2inch4
# from PIL import Image,ImageDraw,ImageFont
# import RPi.GPIO as GPIO

# def rotate_print(self):
#     im_r=self.rotate(180)
#     disp.ShowImage(im_r)

# # lcd gpio configuration:
# RST = 27
# DC = 25
# BL = 24
# bus = 0
# device = 0

# disp = LCD_2inch4.LCD_2inch4(spi=SPI.SpiDev(bus, device),spi_freq=40000000,rst=RST,dc=DC,bl=BL)
# # Initialize library.
# disp.Init()
# # Clear display.
# disp.clear()
# #Display DutyCycle
# disp.bl_DutyCycle(100)
# #Set Fonts
# Font1 = ImageFont.truetype("Font/Font02.ttf",30)
# Font2 = ImageFont.truetype("Font/Font02.ttf",24)
# Font3 = ImageFont.truetype("Font/Font02.ttf",15)
# Font4 = ImageFont.truetype("Font/Font02.ttf",100)

# # Create blank image for drawing
# image = Image.new("RGB", (disp.width, disp.height), "BLACK")
# # draw = ImageDraw.Draw(image)
# draw = ImageDraw.Draw(image)
# #rotate_print(image)
# rotate_print(image)
# time.sleep(1)

# draw.text((75, 5), 'Drag Race', fill = "WHITE",font=Font1)
# # rotate_print(image)
# rotate_print(image)

# #Start Race

# #draw.rectangle([(0,45),(240,320)],fill = "BLACK")
# draw.text((55,100), "Press the button", fill = "WHITE", font=Font2)
# draw.text((55,124), "  to start race ", fill = "WHITE", font=Font2)
# rotate_print(image)

# time.sleep(1)

# # time.sleep(1)

# draw.rectangle([(0,100),(240,320)],fill = "BLACK")
# draw.text((60,100), " Race Start in: ", fill = "WHITE", font=Font2)
# rotate_print(image)

# for x in range(6):
#     draw.rectangle([(95,124),(195,224)],fill = "BLACK")
#     draw.text((94,124), "{}".format(str((5-x))), fill = "RED", font = Font4)
#     rotate_print(image)
#     time.sleep(1)


# draw.rectangle([(0,100),(240,320)],fill = "BLACK")
# draw.text((15,100), "Race Time Left:", fill = "WHITE", font=Font2)
# draw.text((15,200), "Race time Rigth:", fill = "WHITE", font=Font2)

       
# # draw.text((20,60), "{:.3f} s".format(time_stamp_left), fill = "RED", font = Font2)

# draw.text((20,124), "False Start", fill = "RED", font = Font2)

# # draw.text((20,88), "{:.3f} s".format(time_stamp_rigth), fill = "RED", font = Font2)

# draw.text((20,224), "False Start", fill = "RED", font = Font2)

# rotate_print(image)

# time.sleep(2)

# draw.rectangle([(0,100),(240,320)],fill = "BLACK")
# draw.text((55, 100), 'END RACE', fill = "WHITE",font=Font1)

# rotate_print(image)

# time.sleep(2)

# disp.clear()

# disp.module_exit()

# #!/usr/bin/python
# # -*- coding: UTF-8 -*-
# import os
# import sys 
# import time
# import spidev as SPI
# from lib import LCD_1inch3
# from PIL import Image,ImageDraw,ImageFont

# # lcd gpio configuration:
# RST = 27
# DC = 25
# BL = 15
# bus = 0 
# device = 0 

# # Initialize the LCD display
# disp = LCD_1inch3.LCD_1inch3(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
# disp.Init()
# disp.clear()

# # Create a white image for drawing
# image = Image.new("RGB", (disp.width, disp.height), "PURPLE")
# draw = ImageDraw.Draw(image)

# # Draw the white image on the display
# rotate_print(image)

# time.sleep(10)

# disp.module_exit()

#!/usr/bin/python
#-*- coding: UTF-8 -*-
import os
import sys 
import time
import spidev as SPI
from lib import LCD_1inch3
from PIL import Image,ImageDraw,ImageFont

# lcd gpio configuration:
RST = 27
DC = 25
BL = 15
bus = 0 
device = 0 

# Initialize the LCD display
disp = LCD_1inch3.LCD_1inch3(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
disp.Init()
disp.clear()

# Create a black image for drawing
image = Image.new("RGB", (disp.width, disp.height), "BLACK")
draw = ImageDraw.Draw(image)

# # Set the font
# font = ImageFont.truetype("Font/Font01.ttf",25)

# Write a message with white text
draw.text((10, 10), "Hello, World!", fill="WHITE", font=font3)

#Rotate image

im_r=image.rotate(270)

# Draw the image on the display
disp.ShowImage(im_r)

time.sleep(5)

disp.module_exit()
