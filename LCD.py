# #!/usr/bin/python
# # -*- coding: UTF-8 -*-
import os
import sys 
import time
import spidev as SPI
#sys.path.append("..")
from lib import LCD_1inch54
from lib import LCD_1inch3
from PIL import Image,ImageDraw,ImageFont

def rotate_print(self):
    im_r=self.rotate(270)
    disp.ShowImage(im_r)

# lcd gpio configuration:
RST = 27
DC = 25
BL = 15
bus = 0 
device = 0 

disp = LCD_1inch3.LCD_1inch3(spi=SPI.SpiDev(bus, device),spi_freq=1000000000,rst=RST,dc=DC,bl=BL)
#disp = LCD_1inch3.LCD_1inch3()
    # Initialize library.
disp.Init()
    # Clear display.
# disp.clear()

#Set Fonts
Font1 = ImageFont.truetype("Font/Font02.ttf",40)
Font2 = ImageFont.truetype("Font/Font02.ttf",35)
Font3 = ImageFont.truetype("Font/Font02.ttf",20)

# Create blank image for drawing
image = Image.new("HSV", (disp.width, disp.height), "BLACK")
# draw = ImageDraw.Draw(image)
draw = ImageDraw.Draw(image)

time.sleep(5)

draw.text((5, 5), 'Drag Race', fill = "WHITE",font=Font1)
im_r=image.rotate(270)
disp.ShowImage(im_r)

#draw.text((5, 40), 'END RACE', fill = "WHITE",font=Font2)

time.sleep(5)

# im_r=image.rotate(270)
# disp.ShowImage(im_r)

draw.text((5,40), "Race Start in:", fill = "WHITE", font=Font2)

for x in range(6):
    draw.rectangle([(9,74),(41,115)],fill = "BLACK")
    draw.text((10,75), "{}".format(str((5-x))), fill = "RED", font = Font1)
    rotate_print(image)
    time.sleep(1)



time.sleep(20)

disp.clear()

disp.module_exit()

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
# disp.ShowImage(image)

# time.sleep(10)

# disp.module_exit()

#!/usr/bin/python
# -*- coding: UTF-8 -*-
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

# # Create a black image for drawing
# image = Image.new("RGB", (disp.width, disp.height), "BLACK")
# draw = ImageDraw.Draw(image)

# # # Set the font
# # font = ImageFont.truetype("Font/Font01.ttf",25)

# # Write a message with white text
# draw.text((10, 10), "Hello, World!", fill="WHITE", font=font3)

# #Rotate image

# im_r=image.rotate(270)

# # Draw the image on the display
# disp.ShowImage(im_r)

time.sleep(10)

disp.module_exit()
