from importlib import import_module
from tagfinder.output import AccumulatingOutput
from tagfinder.output.pixel_displays import Display
from tagfinder.tag import Detection

from PIL import Image, ImageDraw, ImageFont


class DisplayPixel(AccumulatingOutput):
    def __init__(self, device, height, width, background_color = "white", foreground_color = "black", font = "DejaVuSans", fontsize = 24, rows = 2, columns = 2, line_width = 2, **kwargs) -> None:
        super().__init__(**kwargs)
        self.height = height
        self.width = width
        self.background_color = background_color
        self.foreground_color = foreground_color
        self.font = font
        self.fontsize = fontsize
        self.rows = rows
        self.columns = columns
        self.line_width = line_width
        
        device = device.replace('-', '_')
        class_name = ''.join([x.title() for x in device.split('_')])
        
        self.device : Display = getattr(import_module('tagfinder.output.pixel_displays.' + device), class_name)(height = height, width = width, **kwargs)

    def write(self, tags: "list[Detection]") -> None:
        image = Image.new("RGB", (self.width, self.height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw a filled box as the background
        draw.rectangle((0, 0, self.width - 1, self.height - 1), fill=self.background_color)

        draw.line([(self.width // 2, 0), (self.width // 2, self.height - 1)], fill=self.foreground_color, width=self.line_width)
        draw.line([(0, self.height // 2), (self.width - 1, self.height // 2)], fill=self.foreground_color, width=self.line_width)

        # Load a TTF Font
        font = ImageFont.truetype(self.font, self.fontsize)
        
        text_pos = [
            [1, 1],
            [self.width // 2 + 5, 1],
            [1, self.height // 2 + 1],
            [self.width // 2 + 5, self.height // 2 + 1],
        ]
        
        # Draw Some Text
        for i, tag in enumerate(tags[:4]):
            text = str(tag)
            (font_width, font_height) = font.getsize(text)
            draw.text(
                text_pos[i],
                text,
                font=font,
                fill=self.foreground_color,
            )
            text = str(tag.strength)
            while len(text) < 3:
                text = ' ' + text
            draw.text(
                (text_pos[i][0], text_pos[i][1] + font_height),
                text,
                font=font,
                fill=self.foreground_color,
            )
            
        self.device.draw(image)