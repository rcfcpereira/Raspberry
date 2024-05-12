# lcd_lib.py

from PIL import Image, ImageDraw, ImageFont
import spidev as SPI
from lib import LCD_2inch4

class RaceLCD:
    def __init__(self, BUS=0, DEVICE=0, RST_PIN=27, DC_PIN=25, BL_PIN=24):
        """
        Initialize the RaceLCD class.

        Args:
            BUS (int): The SPI bus number.
            DEVICE (int): The SPI device number.
            RST_PIN (int): The reset pin number for the LCD.
            DC_PIN (int): The data/command pin number for the LCD.
            BL_PIN (int): The backlight pin number for the LCD.

        Returns:
            None
        """
        # lcd gpio configuration:
        self.display = LCD_2inch4.LCD_2inch4(spi=SPI.SpiDev(BUS, DEVICE), spi_freq=40000000, rst=RST_PIN, dc=DC_PIN, bl=BL_PIN)

        self.display.Init()
        self.display.clear()
        self.display.bl_DutyCycle(60)

    def rotate_print(self, image):
        """
        Rotate the image and display it on the LCD.

        Args:
            image (PIL.Image): The image to be rotated and displayed.

        Returns:
            None
        """
        im_r = image.rotate(180)
        self.display.ShowImage(im_r)

    def create_fonts(self):
        """
        Create font objects for drawing text on the LCD.

        Args:
            None

        Returns:
            tuple: A tuple containing font objects for different font sizes.
        """
        Font1 = ImageFont.truetype("Font/Font02.ttf", 30)
        Font2 = ImageFont.truetype("Font/Font02.ttf", 24)
        Font3 = ImageFont.truetype("Font/Font02.ttf", 15)
        Font4 = ImageFont.truetype("Font/Font02.ttf", 100)
        return Font1, Font2, Font3, Font4

    def create_image(self):
        """
        Create a blank image for drawing on the LCD.

        Args:
            None

        Returns:
            tuple: A tuple containing the blank image and the draw object.
        """
        image = Image.new("RGB", (self.display.width, self.display.height), "BLACK")
        draw = ImageDraw.Draw(image)
        self.rotate_print(image)
        return image, draw

    def cleanup_display(self):
        """
        Clean up the LCD display.

        Args:
            None

        Returns:
            None
        """
        self.display.clear()
        self.display.module_exit()