
from PIL import Image, ImageDraw, ImageFont
import spidev as SPI
import smbus
from lib import LCD_2inch4

class RaceLCD:
    def __init__(self,BUS=0, DEVICE=0, RST_PIN=27, DC_PIN=25, BL_PIN=24):

        # lcd gpio configuration:      
        self.display = LCD_2inch4.LCD_2inch4(spi=SPI.SpiDev(BUS, DEVICE), spi_freq=40000000, rst=RST_PIN, dc=DC_PIN, bl=BL_PIN)

        self.image = Image.new("RGB", (self.display.width, self.display.height), "BLACK")
        self.draw = ImageDraw.Draw(self.image)

        # Initialize library.
    def init_display(self, dutty_cycle=60):

        # Initialize library.
        self.display.Init()
        # Clear display.
        self.display.clear()

        # Display DutyCycle
        self.bl_DutyCycle(dutty_cycle)   

    def rotate_print(self):
        img_r=self.image.rotate(180)
        self.draw.ShowImage(img_r)

    # def blank_image(self):
    # # Create blank image for drawing.
    #     image = Image.new("RGB", (self.display.width, self.display.height), "BLACK")
    #     draw = ImageDraw.Draw(image)
    #     return draw
    
    def cleanup_display(self):
        self.clear()
        self.module_exit()
        