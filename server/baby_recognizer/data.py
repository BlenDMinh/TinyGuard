import torch
from config import config
import glob
from pathlib import Path
from PIL import Image
import torchvision.transforms as transforms

data = []

for path in glob.glob(config["DATA_PATH"] + "**/**.jpg", recursive=True):
    _path = Path(path)
    if _path.suffix == '.txt':
        continue

    parent = _path.parent
    name = _path.stem
    if not Path.joinpath(parent, name + ".txt").exists():
        continue

    data.append((path, str(Path.joinpath(parent, name + ".txt"))))

class BabyDataset(torch.utils.data.Dataset):
    def __init__(self, config=config, transform=transforms.Compose([transforms.Resize((448, 448)), transforms.ToTensor()])):
        self.S = config["STRIDE"]
        self.C = config["CLASS_NUM"]
        self.B = config["BOX_NUM_PER_CELL"]
        self.transform = transform
    
    def __len__(self):
        return len(data)
    
    def __getitem__(self, index):
        img_path, label_pth = data[index]
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
