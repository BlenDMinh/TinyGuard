from yolov3_dataset import BabyDataset
from torch.utils.data import DataLoader
import yolov3_config as config
import torch
import torch.optim as optim

from yolov3_model import YOLOv3
from tqdm import tqdm
from yolo3_utils import (
    mean_average_precision,
    cells_to_bboxes,
    get_evaluation_bboxes,
    save_checkpoint,
    load_checkpoint,
    check_class_accuracy,
    get_loaders,
    plot_couple_examples
)
from yolov3_loss import YoloLoss
import warnings
warnings.filterwarnings("ignore")

torch.backends.cudnn.benchmark = True


def train_fn(train_loader, model, optimizer, loss_fn, scaler, scaled_anchors):
    loop = tqdm(train_loader, leave=True)
    losses = []
    for batch_idx, (x, y) in enumerate(loop):
        x = x.to(config.DEVICE)
        y0, y1, y2 = (
            y[0].to(config.DEVICE),
            y[1].to(config.DEVICE),
            y[2].to(config.DEVICE),
        )

        with torch.cuda.amp.autocast():
            out = model(x)
            loss = (
                loss_fn(out[0], y0, scaled_anchors[0])
                + loss_fn(out[1], y1, scaled_anchors[1])
                + loss_fn(out[2], y2, scaled_anchors[2])
            )

        losses.append(loss.item())
        optimizer.zero_grad()
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()

        # update progress bar
        mean_loss = sum(losses) / len(losses)
        loop.set_postfix(loss=mean_loss)
    return mean_loss


def main():
    model = YOLOv3(num_classes=config.CLASS_NUM).to(config.DEVICE)
    optimizer = optim.Adam(
        model.parameters(), lr=config.LEARNING_RATE, weight_decay=config.WEIGHT_DECAY
    )
    loss_fn = YoloLoss()
    scaler = torch.cuda.amp.GradScaler()

    train_dataset = BabyDataset(transform=config.train_transforms)

    train_loader = DataLoader(
        dataset=train_dataset,
        batch_size=config.BATCH_SIZE,
        num_workers=config.NUM_WORKERS,
        pin_memory=config.PIN_MEMORY,
        shuffle=True,
        drop_last=True,
    )

    test_dataset = BabyDataset(
        transform=config.test_transforms, data_csv=config.IMAGE_TEST_CSV)
    test_loader = DataLoader(
        dataset=test_dataset,
        batch_size=config.BATCH_SIZE,
        num_workers=config.NUM_WORKERS,
        pin_memory=config.PIN_MEMORY,
        shuffle=True,
        drop_last=True,
    )

    if config.LOAD_MODEL:
        load_checkpoint(
            config.CHECKPOINT_FILE, model, optimizer, config.LEARNING_RATE
        )

    scaled_anchors = (
        torch.tensor(config.ANCHORS)
        * torch.tensor(config.STRIDE).unsqueeze(1).unsqueeze(1).repeat(1, 3, 2)
    ).to(config.DEVICE)

    losses = []

    for epoch in range(config.NUM_EPOCHS):
        # plot_couple_examples(model, test_loader, 0.6, 0.5, scaled_anchors)
        loss = train_fn(train_loader, model, optimizer,
                        loss_fn, scaler, scaled_anchors)
        losses.append(loss)

        if config.SAVE_MODEL and epoch % 10 == 0:
            save_checkpoint(model, optimizer, filename=f"checkpoint.pth.tar")

        print(f"Currently epoch {epoch}")
        # print("On Train Eval loader:")
        # print("On Train loader:")

        if epoch > 0 and epoch % 30 == 0:
            check_class_accuracy(model, train_loader,
                                 threshold=config.CONF_THRESHOLD)
            check_class_accuracy(model, test_loader,
                                 threshold=config.CONF_THRESHOLD)
            pred_boxes, true_boxes = get_evaluation_bboxes(
                test_loader,
                model,
                iou_threshold=config.NMS_IOU_THRESH,
                anchors=config.ANCHORS,
                threshold=config.CONF_THRESHOLD,
            )
            mapval = mean_average_precision(
                pred_boxes,
                true_boxes,
                iou_threshold=config.MAP_IOU_THRESH,
                box_format="midpoint",
                num_classes=config.CLASS_NUM,
            )
            print(f"mAP: {mapval.item()}")
            model.train()
    save_checkpoint(model, optimizer, filename=f"checkpoint.pth.tar")

    with open('losses.txt', 'w') as f:
        f.write(str(losses))


if __name__ == "__main__":
    main()
