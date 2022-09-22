from importlib import import_module
from tagfinder.output import AccumulatingOutput
from tagfinder.output.text_displays import Display
from tagfinder.tag import Detection

from logging import getLogger

logger = getLogger('tag_finder')

class DisplayText(AccumulatingOutput):
    def __init__(self, device, rows, columns, **kwargs) -> None:
        super().__init__(**kwargs)
        
        self.rows = rows
        self.columns = columns
        
        self.tags_per_row = columns // 5
        
        device = device.replace('-', '_')
        class_name = ''.join([x.title() for x in device.split('_')])
        self.device : Display = getattr(import_module('tagfinder.output.text_displays.' + device), class_name)(rows = rows, columns = columns, **kwargs)

        self.device.write('Welcome', 0)
        self.device.turn_off()
        
    def write(self, tags: "list[Detection]") -> None:
        self.device.clear()
        if not tags:
            self.device.write('nothing there...', 0)
            self.device.turn_off()
            return
        for row in range(0, self.rows, 2):
            curr_tags = tags[row//2 * self.tags_per_row:(row//2 + 1) * self.tags_per_row]
            if not curr_tags:
                return
            id_text = '|'.join([f'{t.tag.tagID:>4}' for t in curr_tags])
            strength_text = '|'.join([f'{t.strength:>4.2g}' for t in curr_tags])
            self.device.write(id_text, row)
            self.device.write(strength_text, row+1)