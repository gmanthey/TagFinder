from math import inf
from statistics import stdev
from tagfinder.tag import Detection, Pulse, Tag
from logging import getLogger

logger = getLogger('tag_finder')

class TagFinder:
    def __init__(self, possible_tags : "list[Tag]", phase : int, pulses_associated : "list[Pulse]") -> None:
        self.possible_tags = possible_tags
        self.phase : int = phase
        self.pulses_associated : "list[Pulse]" = pulses_associated
    
    def add_pulse(self, pulse : Pulse) -> "list[Tag]":
        now_possible : "list[Tag]" = []
        gap = pulse.time - self.pulses_associated[-1].time
        for tag in self.possible_tags:
            if self.phase == 3:
                if abs(tag.period - gap) < 1:
                    now_possible.append(tag)
            else:
                if abs(tag.gaps[self.phase] - gap) < 1:
                    now_possible.append(tag)

        return now_possible

    def still_allive(self, pulse : Pulse) -> bool:
        if self.phase == 3:
            return False
        gap = pulse.time - self.pulses_associated[-1].time
        for tag in self.possible_tags:
            #logger.debug(', '.join([gap, tag.gaps, tag.period, self.phase]))
            if self.phase == 3:
                if gap <= tag.period + 4:
                    return True
            else:
                if gap <= tag.gaps[self.phase] + 1:
                    return True
            
        return False

    def fit(self) -> float:
        return stdev([p.strength for p in self.pulses_associated])
    
    
    
class TagForay():
    def __init__(self, tags : "list[Tag]", **kwargs) -> None:
        self.tagfinders : "list[TagFinder]" = []
        self.all_tags = tags

    def remove_tagfinders(self, pulses_associated):
        new_tagfinders = []
        for tagfinder in self.tagfinders:
            if not any([pulse in tagfinder.pulses_associated for pulse in pulses_associated]):
                new_tagfinders.append(tagfinder)

        self.tagfinders = new_tagfinders

    def add_pulse(self, pulse : Pulse) -> Detection:
        new_tagfinders = []
        for tagfinder in self.tagfinders:
            if tagfinder.still_allive(pulse):
                new_tagfinders.append(tagfinder)

        self.tagfinders = new_tagfinders

        new_tagfinders = [TagFinder(self.all_tags, 0, [pulse])]
        for tagfinder in self.tagfinders:
            new_possible = tagfinder.add_pulse(pulse)
            if new_possible:
                new_tagfinders.append(TagFinder(new_possible, tagfinder.phase + 1, tagfinder.pulses_associated + [pulse]))

        found_tagfinder : TagFinder = None
        best_fit = inf
        best_phase = 0
        
        for tagfinder in new_tagfinders:
            if len(tagfinder.possible_tags) == 1:
                fit = tagfinder.fit()
                phase = tagfinder.phase
                if found_tagfinder is None or phase > best_phase or (phase == best_phase and fit < best_fit):
                    best_fit = fit
                    best_phase = phase
                    found_tagfinder = tagfinder
        
        if found_tagfinder:
            print(best_fit, best_phase, found_tagfinder.pulses_associated[0])
            self.remove_tagfinders(found_tagfinder.pulses_associated)
            self.tagfinders.append(found_tagfinder)
            strength = max([p.strength for p in found_tagfinder.pulses_associated])
            time = min([p.time for p in found_tagfinder.pulses_associated])
            return Detection(found_tagfinder.possible_tags[0], time, strength)
        else:
            self.tagfinders.extend(new_tagfinders)
            return None

    def process(self, pulses : "list[Pulse]") -> "list[Detection]": 
        tags = []
        for pulse in pulses:
            tag = self.add_pulse(pulse)
            if tag:
                tags.append(tag)

        return tags
