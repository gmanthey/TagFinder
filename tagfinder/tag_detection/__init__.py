from importlib import import_module
from tagfinder.output import Output
from tagfinder.tag_detection.devices import RadioDevice
import numpy as np

from tagfinder.tag_detection.pulse_detection import VampPulseDetector
from tagfinder.tag_detection.tag_file_readers import tag_file_reader
from tagfinder.tag_detection.tag_finder import TagFinder, TagForay


class TagDetector:
    def __init__(self, device, tag_file_type, update_frequency, **kwargs) -> None:
        device = device.replace('-', '_')
        class_name = ''.join([x.title() for x in device.split('_')])
        self.radio_reader : RadioDevice = getattr(import_module('tagfinder.tag_detection.devices.' + device), class_name)(update_frequency = update_frequency, **kwargs)
        tag_file_type = tag_file_type.replace('-', '_')
        tag_reader : tag_file_reader = getattr(import_module('tagfinder.tag_detection.tag_file_readers.' + tag_file_type), tag_file_type)
        
        tags = tag_reader(**kwargs)
        
        self.pulse_detector = VampPulseDetector(**kwargs)
        self.tag_foray = TagForay(tags = tags, **kwargs)
        self.update_frequency = update_frequency * 1000 # in ms
        self.now = 0
        
    def run(self, outputs : "list[Output]", data_file=None):
        while True:
            if data_file:
                data = np.load(data_file)
            else:
                data = self.radio_reader.read()
            
            pulses = self.pulse_detector.find_pulses(data)
            
            for pulse in pulses:
                pulse.time += self.now
            
            tags = self.tag_foray.process(pulses)
            
            for output in outputs:
                output.update(self.now)
            
            for tag in tags:
                for output in outputs:
                    output(tag)
                    
            self.now += self.update_frequency

            if data_file:
                break