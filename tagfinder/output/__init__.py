from dataclasses import dataclass
from logging import getLogger
from time import time

from tagfinder.tag import Detection

logger = getLogger('tag_finder')

class Output:
    def __init__(self, **kwargs) -> None:
        pass
    
    def write(self, tag : Detection) -> None:
        raise NotImplemented
    
    def update(self, now : float) -> None:
        pass
    
    def __call__(self, tag : Detection) -> None:
        self.write(tag)
        
    def close(self):
        pass

class AccumulatingOutput(Output):
    def __init__(self, max_display_time = 30, **kwargs) -> None:
        super().__init__(**kwargs)
        self.tags : "dict[int,Detection]" = {}
        self.max_time = max_display_time * 1000 # in ms
        
    def update(self, now: float) -> None:
        needs_update = False
        new_tags = {}
        
        for tag in self.tags:
            if now - self.tags[tag].time > self.max_time:
                needs_update = True
            else:
                new_tags[tag] = self.tags[tag]
        
        if needs_update:
            self.tags = new_tags
            self.write(sorted(self.tags.values(), key=lambda x: x.time))
        
    def write(self, tags : "list[Detection]") -> None:
        raise NotImplemented

    def __call__(self, tag: Detection) -> None:
        self.tags[tag.tag.tagID] = tag

        self.write(sorted(self.tags.values(), key=lambda x: x.time))
