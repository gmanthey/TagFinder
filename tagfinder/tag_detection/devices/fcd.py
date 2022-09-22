from subprocess import run
import numpy as np
from tagfinder.tag_detection.devices import RadioDevice
from logging import getLogger

import sounddevice as sd

logger = getLogger('tagfinder')

# Samplerate is fixed for fcd
SAMPLERATE = 48000

class Fcd(RadioDevice):
    def __init__(self, frequency, update_frequency, **kwargs) -> None:
        super().__init__()
        run(['fcd', '-q', '-s', str(frequency)])
        self.rec = sd.InputStream(samplerate=SAMPLERATE, blocksize=SAMPLERATE, device = 1, channels=2)
        self.rec.start()
        self.read_amount = SAMPLERATE * update_frequency
        
    def read(self) -> np.ndarray:
        data, overflowed = self.rec.read(self.read_amount)
        
        if overflowed:
            logger.warning(f'Overflow in fcd reading detected, we have lost some data and may have missed a tag! This is most likely due to long processing times')
        
        return data