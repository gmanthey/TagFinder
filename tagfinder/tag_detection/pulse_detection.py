from logging import getLogger
import numpy as np
from tagfinder.tag import Pulse
import vamp

logger = getLogger('tag_finder')

class VampPulseDetector:
    def __init__(self, **kwargs) -> None:
        pass
    
    def find_pulses(self, data : np.ndarray) -> "list[Pulse]":
        data = data.T

        vamp_res = vamp.collect(data, 48000, "lotek-plugins:findpulsefd_2013_final")
        
        res = []
        
        for p in vamp_res['list']:
            timestamp = float(p['timestamp']) * 1000
            
            label = p['label']
            label = {item.strip().split(':')[0]:item.strip().split(':')[1] for item in label.split(';') if ':' in item}
            
            strength = float(label['sig'].strip().split()[0])
                        
            res.append(Pulse(timestamp, strength))

            logger.debug(res[-1])
            
        return res