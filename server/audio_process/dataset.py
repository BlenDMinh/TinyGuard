import os
from torch.utils.data import Dataset
import torchaudio

from audio_utils import CLASS_MAPPING
import csv


class CryDataset(Dataset):

    def __init__(self,
                 transformation,
                 device,
                 csv_path):
        self.device = device
        self.transformation = transformation.to(self.device)
        self.annotations = []
        with open(csv_path) as f:
            reader = csv.reader(f)
            for data in reader:
                self.annotations.append(data)
        # classes = os.listdir(audio_dir)
        # for _cls in classes:
        #     src_dir = os.path.join(audio_dir, _cls)
        #     for fn in os.listdir(src_dir):
        #         self.annotations.append(
        #             [CLASS_MAPPING.index(_cls), os.path.join(src_dir, fn)])

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, index):
        audio_sample_path = self._get_audio_sample_path(index)
        label = int(self._get_audio_sample_label(index))
        signal, sr = torchaudio.load(audio_sample_path)
        signal = signal.to(self.device)
        signal = self.transformation(signal)
        return signal, label

    def _get_audio_sample_path(self, index):
        return self.annotations[index][1]

    def _get_audio_sample_label(self, index):
        return self.annotations[index][0]


if __name__ == "__main__":
    data = []
    classes = os.listdir("clean")
    for _cls in classes:
        src_dir = os.path.join("clean", _cls)
        for fn in os.listdir(src_dir):
            data.append([CLASS_MAPPING.index(_cls), os.path.join(src_dir, fn)])
            # self.annotations.append(
            #     [CLASS_MAPPING.index(_cls), os.path.join(src_dir, fn)])
    import random
    random.shuffle(data)

    n = len(data)

    train_data = data[:int(6*n/10)]
    val_data = data[int(6*n/10):int(6*n/10)+int(3*n/10)]
    test_data = data[int(6*n/10)+int(3*n/10):]

    with open('train_data.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\r')
        writer.writerows(train_data)
    with open('val_data.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\r')
        writer.writerows(val_data)
    with open('test_data.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\r')
        writer.writerows(test_data)
