from pathlib import Path
import cv2
import numpy as np
from yolo3_utils import cells_to_bboxes, non_max_suppression, plot_image
from yolov3_model import YOLOv3
import yolov3_config as config
import torch
from PIL import Image
import albumentations as A
from albumentations.pytorch import ToTensorV2

model = YOLOv3(num_classes=config.CLASS_NUM).to(config.DEVICE)
checkpoint = torch.load('checkpoint.pth.tar',
                        map_location=config.DEVICE)
model.load_state_dict(checkpoint["state_dict"])

image = np.array(Image.open(
    './dataset/test/z4807708284896_33c54a53504037dead358fdd0894df9a.jpg').convert('RGB'))
transforms = A.Compose(
    [
        A.LongestMaxSize(max_size=config.IMAGE_SIZE),
        A.PadIfNeeded(
            min_height=config.IMAGE_SIZE, min_width=config.IMAGE_SIZE, border_mode=cv2.BORDER_CONSTANT
        ),
        A.Normalize(mean=[0, 0, 0], std=[1, 1, 1], max_pixel_value=255,),
        ToTensorV2(),
    ],
)
image = transforms(image=image)['image']
anchors = (
    torch.tensor(config.ANCHORS)
    * torch.tensor(config.STRIDE).unsqueeze(1).unsqueeze(1).repeat(1, 3, 2)
).to(config.DEVICE)
with torch.no_grad():
    out = model(image.unsqueeze(0).to(config.DEVICE))
    bboxes = [[] for _ in range(image.shape[0])]
    for i in range(3):
        batch_size, A, S, _, _ = out[i].shape
        anchor = anchors[i]
        boxes_scale_i = cells_to_bboxes(
            out[i], anchor, S=S, is_preds=True
        )
        for idx, (box) in enumerate(boxes_scale_i):
            bboxes[idx] += box
nms_boxes = non_max_suppression(
    bboxes[0], iou_threshold=0.5, threshold=0.6, box_format="midpoint",
)
print(nms_boxes)
plot_image(image.permute(1, 2, 0).detach().cpu(), nms_boxes)


def draw_box(image, bboxs):
    width, height, _ = image.shape
    for box in bboxs:
        pred_class = "Crying" if box[0] < 1 else "Not Crying"
        box = box[2:]
        if box[2] > 10000 or box[3] > 10000:
            continue
        assert len(box) == 4, "Got more values than in x, y, w, h, in a box!"
        x = int((box[0] - box[2] / 2) * width)
        y = int((box[1] - box[3] / 2) * height)
        w = int(width * box[2])
        h = int(height * box[3])
        image = cv2.rectangle(
            image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        image = cv2.putText(image, pred_class, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
    return image


frame_step = 1
VIDEO_PATH = Path('./dataset/test/video.mp4')


def plot_video():
    image_counter = 0
    read_counter = 0
    src = cv2.VideoCapture(str(VIDEO_PATH))
    video_name = VIDEO_PATH.stem
    result = cv2.VideoWriter(f'./{VIDEO_PATH.parent}/{video_name}_out.avi',
                             -1,
                             30, (416, 416))

    while src.isOpened():
        ret, img = src.read()
        if ret and read_counter % frame_step == 0:
            converted = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cv2.imshow('Before', img)
            x = transforms(image=converted)[
                'image'].unsqueeze(0).to(config.DEVICE)
            y = model(x)
            trans_img = x[0].permute(1, 2, 0).cpu().numpy()
            trans_img = cv2.cvtColor(trans_img, cv2.COLOR_RGB2BGR)
            bboxes = [[] for _ in range(x.shape[0])]
            for i in range(3):
                batch_size, A, S, _, _ = y[i].shape
                anchor = anchors[i]
                boxes_scale_i = cells_to_bboxes(
                    y[i], anchor, S=S, is_preds=True
                )
                for idx, (box) in enumerate(boxes_scale_i):
                    bboxes[idx] += box
            nms_boxes = non_max_suppression(
                bboxes[0], iou_threshold=0.5, threshold=0.7, box_format="midpoint",
            )
            image = draw_box(trans_img, nms_boxes)
            image = cv2.resize(image, (416, 416))
            result.write(image)
            cv2.imshow('Frame', image)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            image_counter += 1
        elif not ret:
            break
        read_counter += 1
    src.release()
    result.release()


# plot_video()
