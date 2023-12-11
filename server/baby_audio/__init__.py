import os
import random
import torch
import torchaudio
from torch import nn
from torchaudio import transforms

SAMPLE_RATE = 16000
DELTA_TIME = 5
CLASS_MAPPING = [
    "Cry",
    "Laugh",
    "Silence"
]
NUM_CLASSES = len(CLASS_MAPPING)
BATCH_SIZE = 64
EPOCHS = 101
LEARNING_RATE = 0.000002
N_MELS = 64
NFFT = 2048
N_MFCC = 24
HOP_LEN = int(10*(10**-3)*SAMPLE_RATE)
WIN_LEN = int(30*(10**-3)*SAMPLE_RATE)
WIN_FN = torch.hamming_window

class AudioUtil():
  @staticmethod
  def time_shift(sig, shift_limit):
   _, sig_len = sig.shape
   shift_amt = int(random.random() * shift_limit * sig_len)
   return sig.roll(shift_amt)

  @staticmethod
  def spectro_gram():
    spectrogram = torchaudio.transforms.MelSpectrogram(
      sample_rate=SAMPLE_RATE,
      n_fft=NFFT,
      hop_length=HOP_LEN,
      win_length=WIN_LEN,
      n_mels=N_MELS,
      window_fn=WIN_FN
    )
    # spectrogram = torchaudio.transforms.AmplitudeToDB()(spectrogram)
    return (spectrogram)
#   @staticmethod
#   def spectro_gram():
#     spectrogram = torchaudio.transforms.MFCC(
#     sample_rate=SAMPLE_RATE,
#     n_mfcc=N_MFCC,
#     melkwargs={'n_fft': NFFT,
#               'hop_length': HOP_LEN,
#               'win_length': WIN_LEN,
#               'n_mels': N_MELS,
#               'window_fn': WIN_FN}
#     )
    return spectrogram

  @staticmethod
  def spectro_augment(spec, max_mask_pct=0.1, n_freq_masks=1, n_time_masks=1):
    _, n_mels, n_steps = spec.shape
    mask_value = spec.mean()
    aug_spec = spec

    freq_mask_param = max_mask_pct * n_mels
    for _ in range(n_freq_masks):
        aug_spec = transforms.FrequencyMasking(freq_mask_param)(aug_spec, mask_value)

    time_mask_param = max_mask_pct * n_steps
    for _ in range(n_time_masks):
        aug_spec = transforms.TimeMasking(time_mask_param)(aug_spec, mask_value)

    return aug_spec

# Model used

class AlexNet(nn.Module):
    """Based on https://github.com/pytorch/vision/blob/master/torchvision/models/alexnet.py
    """

    def __init__(self, num_classes: int = 1000) -> None:
        super(AlexNet, self).__init__()
        self.features = nn.Sequential(
            # Replaced 3-channel with 1, strid=4 with (1,2)
            nn.Conv2d(1, 64, kernel_size=11, stride=(1, 2), padding=2),
            nn.BatchNorm2d(64),  # Added according to the paper.
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(64, 192, kernel_size=5, padding=2),
            nn.BatchNorm2d(192),  # Added according to the paper.
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(192, 384, kernel_size=3, padding=1),
            nn.BatchNorm2d(384),  # Added according to the paper.
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),  # Added according to the paper.
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),  # Added according to the paper.
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
        )
        # Replaced: n.AdaptiveAvgPool2d((6, 6))
        self.avgpool = nn.AdaptiveAvgPool2d((4, 6))
        self.classifier = nn.Sequential(
            nn.Dropout(),
            nn.Linear(256 * 4 * 6, 4096),  # Replaced: 256 * 6 * 6
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, num_classes),
            nn.Softmax(dim=1)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

model = None

def _load_model(path="model.pth"):
    global model
    model = AlexNet(num_classes=NUM_CLASSES).to(device='cuda')
    state_dict = torch.load(os.path.join(os.path.dirname(
        __file__), path), map_location=torch.device('cuda'))
    model.load_state_dict(state_dict)
    return model

def predict_one(waveform, CLASS_MAPPING=CLASS_MAPPING):
    global model
    if model == None:
        model = _load_model()
    model.eval()
    input = AudioUtil.spectro_gram()(waveform).unsqueeze(0).to('cuda')
    with torch.no_grad():
        predictions = model(input)
        predicted_index = predictions[0].argmax(0)
        if predicted_index < 0 or predicted_index >= NUM_CLASSES:
            print("Predicted index is out of range.")
            return None
        predicted = CLASS_MAPPING[predicted_index]
    print(predictions)
    return predicted, predictions[0][predicted_index].item()