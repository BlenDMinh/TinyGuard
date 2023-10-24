import os
from torch.utils.data import Dataset
import torchaudio

from audio_utils import CLASS_MAPPING


class CryDataset(Dataset):

    def __init__(self,
                 transformation,
                 device,
                 audio_dir):
        self.device = device
        self.transformation = transformation.to(self.device)
        self.annotations = []
        classes = os.listdir(audio_dir)
        for _cls in classes:
            src_dir = os.path.join(audio_dir, _cls)
            for fn in os.listdir(src_dir):
                self.annotations.append(
                    [CLASS_MAPPING.index(_cls), os.path.join(src_dir, fn)])

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, index):
        audio_sample_path = self._get_audio_sample_path(index)
        label = self._get_audio_sample_label(index)
        signal, sr = torchaudio.load(audio_sample_path)
        signal = signal.to(self.device)
        signal = self.transformation(signal)
        return signal, label

    def _get_audio_sample_path(self, index):
        return self.annotations[index][1]

    def _get_audio_sample_label(self, index):
        return self.annotations[index][0]
