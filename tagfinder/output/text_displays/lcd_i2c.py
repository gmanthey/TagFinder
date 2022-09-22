from tagfinder.output.text_displays import Display

from rpi_lcd import LCD

class LcdI2C(Display):
    def __init__(self, i2c_address = 0x3f, **kwargs) -> None:
        super().__init__()
        
        self.device = LCD(address = i2c_address)
        
    def write(self, text, row):
        self.device.backlight(True)
        self.device.text(text, row + 1)
        
    def turn_off(self):
        self.device.backlight(False)
        
    def clear(self):
        self.device.clear()