class BoundingBox:
    def __init__(self, x, y, w, h, label, confidence) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.label = label
        self.confidence = confidence

    def to_json(self):
        return dict(x=self.x, y=self.y, w=self.w, h=self.h, label=self.label, confidence=self.confidence)


class ImagePredict:
    def __init__(self, bboxes: list[BoundingBox]) -> None:
        self.bboxes = bboxes

    def to_json(self):
        return dict(bboxes=list(map(lambda e: e.to_json(), self.bboxes)))


class AudioPredict:
    pass
