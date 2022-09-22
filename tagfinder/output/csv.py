from tagfinder.output import Output
from tagfinder.tag import Detection


class Csv(Output):
    def __init__(self, file = "detections.csv", **kwargs) -> None:
        super().__init__(**kwargs)
        self.file = open(file, 'a')

    def write(self, tag: Detection) -> None:
        self.file.write(','.join([str(tag.time), str(tag.tag.tagID)]))
        self.file.flush()
        
    def close(self):
        self.file.close()