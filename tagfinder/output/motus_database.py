from tagfinder.output import Output


class MotusDatabase(Output):
    def __init__(self, file = "detections.sql", **kwargs) -> None:
        super().__init__(**kwargs)

    def write(self, tag: Tag) -> None:
        ...