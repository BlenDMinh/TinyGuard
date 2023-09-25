from model import YoloV1
import torch.optim as optim
from loss import YoloLoss
from config import config
from utils import (
    non_max_suppression,
    mean_average_precision,
    intersection_over_union,
    cellboxes_to_boxes,
    get_bboxes,
    plot_image,
    save_checkpoint,
    load_checkpoint,
)
import torch
from data import BabyDataset

# Hyperparameters etc. 
LEARNING_RATE = 2e-5
# DEVICE = "cuda" if torch.cuda.is_available else "cpu"
DEVICE = "cpu"
BATCH_SIZE = 8 # 64 in original paper but I don't have that much vram, grad accum?
WEIGHT_DECAY = 0
EPOCHS = 1000
NUM_WORKERS = 2
PIN_MEMORY = True
LOAD_MODEL = True
LOAD_MODEL_FILE = "model.pth.tar"

model = YoloV1(split_size=config["STRIDE"], num_boxes=config["BOX_NUM_PER_CELL"], num_classes=config["CLASS_NUM"]).to(DEVICE)
optimizer = optim.Adam(
    model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY
)
loss_fn = YoloLoss()

if LOAD_MODEL:
    load_checkpoint(torch.load(LOAD_MODEL_FILE), model, optimizer)

data = BabyDataset()

img = data[4][0]
predict = model(img.unsqueeze(0))

boxes = cellboxes_to_boxes(predict)
print(boxes)
# plot_image(img, boxes[:8])
