import json


class BoundingBox:
    def __init__(self, x, y, w, h, label, confidence) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.label = label
        self.confidence = confidence

    def to_json(self, to_string: bool = False) -> dict[str, any] | str:
        json_obj = dict(x=self.x, y=self.y, w=self.w, h=self.h,
                        label=self.label, confidence=self.confidence)
        if to_string:
            return json.dumps(json_obj)
        return json_obj


class ImagePredict:
    def __init__(self, bboxes: list[BoundingBox]) -> None:
        self.bboxes = bboxes
        is_crying = False
        for bbox in bboxes:
            is_crying = is_crying or bbox.label == 0
        self.is_crying = is_crying

    def to_json(self, to_string: bool) -> dict[str, any] | str:
        json_obj = dict(bboxes=list(map(lambda e: e.to_json(),
                        self.bboxes)), is_crying=self.is_crying)
        if to_string:
            return json.dumps(json_obj)
        return json_obj


class AudioPredict:
    pass
