import torch
from config import config
import glob
from pathlib import Path
from PIL import Image
import torchvision.transforms as transforms
from torch.utils.data import Dataset

# data = []

# for path in glob.glob(config["DATA_PATH"] + "**/**.jpg", recursive=True):
#     _path = Path(path)
#     if _path.suffix == '.txt':
#         continue

#     parent = _path.parent
#     name = _path.stem
#     if not Path.joinpath(parent, name + ".txt").exists():
#         continue

#     data.append((path, str(Path.joinpath(parent, name + ".txt"))))

class BabyDataset(Dataset):
    def __init__(self, config=config, transform=transforms.Compose([transforms.Resize((448, 448)), transforms.ToTensor()])):
        self.S = config["STRIDE"]
        self.C = config["CLASS_NUM"]
        self.B = config["BOX_NUM_PER_CELL"]
        self.transform = transform

        self._image_data = []

        with open(config['image_data_csv']) as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                self._image_data.append(row)
    
    def __len__(self):
        return len(self._image_data)
    
    def __getitem__(self, index):
        img_path, label_pth = self._image_data[index]
        boxes = []
        with open(label_pth, "r") as f:
            for label in f.readlines():
                class_label, xc, yc, w, h = label.replace("\n", "").split()
                class_label = int(class_label)
                xc, yc, w, h = map(float, [xc, yc, w, h])
                boxes.append([class_label, xc, yc, w, h])
        
        image = Image.open(img_path).convert("RGB")
        boxes = torch.tensor(boxes)

        if self.transform != None:
            image = self.transform(img=image)
        
        label_matrix = torch.zeros((self.S, self.S, self.C + self.B * 5))

        for box in boxes:
            class_label, xc, yc, w, h = box.tolist()
            class_label = int(class_label)

            j, i = int(xc * self.S), int(yc * self.S)
            x_cell, y_cell = xc * self.S - j, yc * self.S - i
            w_cell, h_cell = w * self.S, h * self.S

            # 0 -> C - 1: class
            if label_matrix[i, j, self.C] == 0:
                label_matrix[i, j, self.C] = 1
                box_coord = torch.tensor([x_cell, y_cell, w_cell, h_cell])
                label_matrix[i, j, self.C + 1 : self.C + 5] = box_coord
                label_matrix[i, j, class_label] = 1
        return image, label_matrix

class TinyGuardianBabyDataset(Dataset):
    def __init__(self, config=config, transform=transforms.Compose([transforms.Resize((448, 448)), transforms.ToTensor()])):
        super().__init__()
        self.S = config['stride']
        self.C = config['class_num']
        self.B = config['box_num']
        self.transform = transform

        self._image_data = [None]
        self._audio_data = [None]

        with open(config['image_data_csv']) as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                self._image_data.append(row)
        with open(config['audio_data_csv']) as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                self._audio_data.append(row)
    
    @classmethod
    def _class_calc(cls, img_class=-1, aud_class=-1):
        # no image and audio
        if img_class == -1 and aud_class == -1:
            return 0
        if img_class == -1:
            return aud_class
        if aud_class == -1:
            return img_class
        factor = config['audio_data_factor']
        prob = img_class * (1 - factor) + aud_class * factor
        return 1 if prob >= config['data_threshold'] else 0

    # TODO: pair each image and audio, return the number of pair?
    def __len__(self):
        return len(self._image_data) * len(self._audio_data)
    
    def __getitem__(self, index):
        img_index = index / len(aud_index)
        aud_index = index % len(aud_index)

        img_data = self._image_data[img_index]
        aud_data = self._audio_data[aud_index]

        if img_data == None:
            image = Image.new('RGB', (448, 448))
            img_class_label = -1
        else:
            img_path, label_pth = img_data
            image = Image.open(img_path).convert("RGB")

        if aud_data == None:

            aud_class_label = -1
        else:
            pass

        boxes = []
        if img_class_label != -1:
            with open(label_pth, "r") as f:
                for label in f.readlines():
                    class_label, xc, yc, w, h = label.replace("\n", "").split()
                    class_label = int(class_label)
                    class_label = TinyGuardianBabyDataset._class_calc(img_class=class_label, aud_class=aud_class_label)
                    xc, yc, w, h = map(float, [xc, yc, w, h])
                    boxes.append([class_label, xc, yc, w, h])
        
        boxes = torch.tensor(boxes)

        if self.transform != None:
            image = self.transform(img=image)
        
        label_matrix = torch.zeros((self.S, self.S, self.C + self.B * 5))

        for box in boxes:
            class_label, xc, yc, w, h = box.tolist()
            class_label = int(class_label)

            j, i = int(xc * self.S), int(yc * self.S)
            x_cell, y_cell = xc * self.S - j, yc * self.S - i
            w_cell, h_cell = w * self.S, h * self.S

            # 0 -> C - 1: class
            if label_matrix[i, j, self.C] == 0:
                label_matrix[i, j, self.C] = 1
                box_coord = torch.tensor([x_cell, y_cell, w_cell, h_cell])
                label_matrix[i, j, self.C + 1 : self.C + 5] = box_coord
                label_matrix[i, j, class_label] = 1
        return image, label_matrix

import csv

def preprocess_csv(config=config):
    with open(config['image_data_csv'], 'w') as f:
        writer = csv.writer(f, lineterminator='\r')
        for path in glob.glob(config["image_data_path"] + "**/**.jpg", recursive=True):
            _path = Path(path)
            if _path.suffix == '.txt':
                continue

            parent = _path.parent
            name = _path.stem
            if not Path.joinpath(parent, name + ".txt").exists():
                continue
        

            writer.writerow([str(_path), str(Path.joinpath(parent, name + ".txt"))])
    with open(config['audio_data_csv'], 'w') as f:
        writer = csv.writer(f, lineterminator='\r')
        for path in glob.glob(config['audio_data_path'] + "Cry/" + "**/**.wav", recursive=True):
            writer.writerow([str(Path(path)), 0])
        for path in glob.glob(config['audio_data_path'] + "NoCry/" + "**/**.wav", recursive=True):
            writer.writerow([str(Path(path)), 1])

if __name__ == "__main__":
    preprocess_csv()
    # baby = TinyGuardianBabyDataset()