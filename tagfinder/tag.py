from dataclasses import dataclass

@dataclass 
class Pulse():
    time : float
    strength : int

@dataclass 
class Tag:
    tagID : int
    gaps : "list[float]"
    period : float

    def __str__(self) -> str:
        return str(self.tagID)

@dataclass
class Detection:
    tag : Tag
    time : float
    strength : int