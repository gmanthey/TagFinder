from collections import namedtuple
from tagfinder.output.pixel_displays import Display
from adafruit_epd.ssd1680 import Adafruit_SSD1680
import digitalio
import busio
import board
from PIL import Image

class SSD1680(Display):
    def __init__(self, height, width, rotation = 1, cs_pin = 17, dc_pin = 22, rst_pin = None, busy_pin = None, sramcs_pin = None) -> None:
        super().__init__()
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        Pin = namedtuple("Pin", ['id'])
        cs = digitalio.DigitalInOut(Pin(cs_pin))
        dc = digitalio.DigitalInOut(Pin(dc_pin))
        rst = digitalio.DigitalInOut(Pin(rst_pin)) if rst_pin else None
        busy = digitalio.DigitalInOut(Pin(busy_pin)) if busy_pin else None
        sramcs = digitalio.DigitalInOut(Pin(sramcs_pin)) if sramcs_pin else None
        
        self.display = Adafruit_SSD1680(122, 250, spi, cs_pin=cs, dc_pin=dc, sramcs_pin=sramcs, rst_pin=rst, busy_pin=busy)
        
        self.display.rotation = rotation
        
    def draw(self, image: Image.Image):
        self.display.image(image)
        self.display.display()