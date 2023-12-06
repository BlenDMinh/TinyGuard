import torchaudio
import torch
import json
# from audio_process.audio_utils import DELTA_TIME, SAMPLE_RATE
from entity.device import Device
# from audio_process.predict import predict_one


class BoundingBox:
    def __init__(self, x, y, w, h, label, confidence) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.label = int(label)
        self.confidence = confidence

    def to_json(self, to_string: bool = False) -> dict[str, any] | str:
        json_obj = dict(x=self.x, y=self.y, w=self.w, h=self.h,
                        label=self.label, confidence=self.confidence)
        if to_string:
            return json.dumps(json_obj)
        return json_obj


class ImagePredict:
    def __init__(self, bboxes: list[BoundingBox], device: Device = None) -> None:
        self.bboxes = bboxes
        self.device = device
        is_crying = False
        for bbox in bboxes:
            is_crying = is_crying or bbox.label == 0
        self.is_crying = is_crying

    def to_json(self, to_string: bool = False) -> dict[str, any] | str:
        json_obj = dict(
            device=self.device.to_json() if self.device else Device(code="test").to_json(),
            bboxes=list(map(lambda e: e.to_json(),
                        self.bboxes)),
            is_crying=self.is_crying)
        if to_string:
            return json.dumps(json_obj)
        return json_obj


THRESHOLD = 0.15


def envelope(y, rate, threshold):
    mask = []
    window_size = int(rate / 20)
    y_abs = torch.abs(y)
    y_abs = torch.nn.functional.pad(y_abs, (0, window_size-1))
    y_mean = y_abs.unfold(0, window_size, 1).max(1).values
    mask = y_mean > threshold
    return mask


# def downsample_mono(waveform, sample_rate, sr):
#     if waveform.shape[0] > 1:
#         waveform = torch.mean(waveform, dim=0, keepdim=True)
#     if sample_rate != sr:
#         resampler = torchaudio.transforms.Resample(
#             orig_freq=sample_rate, new_freq=sr)
#         waveform = resampler(waveform)
#     return sr, waveform


def truncate(wavform):
    delta_sample = int(DELTA_TIME*SAMPLE_RATE)
    mask = envelope(wavform.reshape(-1), SAMPLE_RATE, THRESHOLD)
    wav = wavform[:, mask]
    length_signal = wav.shape[1]
    if length_signal < delta_sample:
        wav = torch.nn.functional.pad(
            wav, (0, delta_sample-length_signal))
        return wav
    else:
        return wav[:, :DELTA_TIME*SAMPLE_RATE]


class AudioPredict:
    def __init__(self, wavform) -> None:
        self.wav = truncate(wavform=wavform)

    def to_json(self, to_string: bool = False) -> dict[str, any] | str:
        prediction = predict_one(waveform=self.wav)
        json_obj = dict(prediction=prediction)
        if to_string:
            return json.dumps(json_obj)
        return json_obj
