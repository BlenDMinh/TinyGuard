import os
import torch
import torchaudio
from torch import nn

DELTA_TIME = 5
SAMPLE_RATE = 16000
CLASS_MAPPING = [
    # "Cat",
    # "ChurchBell",
    "Cry",
    # "Dog",
    "Laugh",
    # "Rain",
    "Silence",
    # "WaterDrop",
    # "Wind"
]
N_MELS = 64
NFFT = 2048
HOP_LEN = int(10*(10**-3)*SAMPLE_RATE)
WIN_LEN = int(30*(10**-3)*SAMPLE_RATE)
NUM_CLASSES = len(CLASS_MAPPING)

mel_spectrogram = torchaudio.transforms.MelSpectrogram(
    sample_rate=SAMPLE_RATE,
    n_fft=NFFT,
    hop_length=HOP_LEN,
    win_length=WIN_LEN,
    n_mels=N_MELS
)

# Model used

class CNNNetwork(nn.Module):

    def __init__(self):
        super(CNNNetwork, self).__init__()

        # 1st conv layer
        self.conv1 = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(32)
        )

        # 2nd conv layer
        self.conv2 = nn.Sequential(
            nn.Conv2d(32, 32, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(32)
        )

        # 3rd conv layer
        self.conv3 = nn.Sequential(
            nn.Conv2d(32, 32, kernel_size=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=1),
            nn.BatchNorm2d(32)
        )

        # Fully connected layers
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32000, 64),  # Adjust input size based on your data
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, NUM_CLASSES),
            nn.Softmax(dim=1)
        )

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.fc(x)
        return x

model = None

def _load_model(path="model.pth"):
    global model
    model = CNNNetwork()
    state_dict = torch.load(os.path.join(os.path.dirname(
        __file__), path), map_location=torch.device('cuda'))
    model.load_state_dict(state_dict)
    return model

def predict_one(waveform, CLASS_MAPPING=CLASS_MAPPING):
    global model
    if model == None:
        model = _load_model()
    model.eval()
    input = mel_spectrogram(waveform).unsqueeze(0)
    with torch.no_grad():
        predictions = model(input)
        print(predictions)
        predicted_index = predictions[0].argmax(0)
        if predicted_index < 0 or predicted_index >= NUM_CLASSES:
            print("Predicted index is out of range.")
            return None
        predicted = CLASS_MAPPING[predicted_index]
    return predicted