import cv2
import os
import pathlib
from matplotlib import pyplot
from matplotlib.patches import Rectangle
import numpy as np
import shutil

SRC_PATH = "./src1/"

paths = os.listdir(path=SRC_PATH)
paths = list(filter(lambda x: pathlib.Path(x).suffix == '.jpg', paths))
paths = list(map(lambda x: x.split('.')[0], paths))

# print(paths[0].split())


def plotData(img, box):
    fig, ax = pyplot.subplots()
    ax.imshow(img)
    ax.add_patch(Rectangle(
        (len(img[0]) * box[0] - len(img[0]) * box[2] /
         2, len(img) * box[1] - len(img) * box[3] / 2),
        width=len(img[0]) * box[2],
        height=len(img) * box[3],
        fill=None
    ))
    pyplot.show()


def filter_one(img):
    img = cv2.filter2D(img, ddepth=-1, kernel=np.ones((5, 5)) / 25)
    return img


def filter_two(img):
    kernel = np.random.rand(5, 5)
    kernel = kernel / (np.sum(kernel) / 1.1)
    img = cv2.filter2D(
        img, ddepth=-1, kernel=kernel)
    return img


def filter_three(img):
    print(img.shape)
    noise = np.zeros(img.shape, np.uint8)
    noise = cv2.randn(noise, 0, 255)
    img = cv2.add(img, noise)
    return img


def filter_four(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return gray_img


filters = [filter_one, filter_two, filter_three]

for path in paths:
    impath = SRC_PATH + path + ".jpg"
    img = cv2.imread(impath)

    labelpath = SRC_PATH + path + ".txt"
    box = []
    with open(labelpath, "r") as f:
        box = f.readline()
        box = list(map(float, box.split()))[1: len(box)]
    if len(box) < 4:
        continue

    for id, filter in enumerate(filters):
        new_img = filter(img)
        cv2.imwrite(SRC_PATH + f'filters/{path}_{id}.jpg', new_img)
        shutil.copyfile(labelpath, SRC_PATH + f'filters/{path}_{id}.txt')
