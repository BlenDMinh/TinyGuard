import glob
import cv2
import os
import pathlib
from matplotlib import pyplot
import numpy as np
import shutil

SRC_PATH = "./src1/"

paths = glob.glob(SRC_PATH + "**/**.jpg", recursive=True)
print(paths)

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
    _path = pathlib.Path(path)
    
    parent = _path.parent
    name = _path.stem
    if not pathlib.Path.joinpath(parent, name + ".txt").exists():
        open(pathlib.Path.joinpath(parent, name + ".txt"), 'x')
    
    impath = str(pathlib.Path.joinpath(parent, name + ".jpg"))
    img = cv2.imread(impath)
    labelpath = str(pathlib.Path.joinpath(parent, name + ".txt"))
    box = []
    with open(labelpath, "r") as f:
        box = f.readline()
        box = list(map(float, box.split()))[1: len(box)]
    # if len(box) < 4:
    #     continue
    
    # Specify the kernel size. 
    # The greater the size, the more the motion. 
    kernel_size = max([int(max(img.shape) * 1.5 / 100), 1])
    
    # Create the vertical kernel. 
    kernel_v = np.zeros((kernel_size, kernel_size)) 
    
    # Create a copy of the same for creating the horizontal kernel. 
    kernel_h = np.copy(kernel_v) 
    
    # Fill the middle row with ones. 
    kernel_v[:, int((kernel_size - 1)/2)] = np.ones(kernel_size) 
    kernel_h[int((kernel_size - 1)/2), :] = np.ones(kernel_size) 
    
    # Normalize. 
    kernel_v /= kernel_size 
    kernel_h /= kernel_size 
    
    # Apply the vertical kernel. 
    vertical_mb = cv2.filter2D(img, -1, kernel_v) 
    
    # Apply the horizontal kernel. 
    horizonal_mb = cv2.filter2D(img, -1, kernel_h)
    
    print(f"Making ./filters/{parent.stem}/{name}")
    
    pathlib.Path(f"./filters/{parent.stem}").mkdir(parents=True, exist_ok=True)
    
    # Save the outputs. 
    cv2.imwrite(f"./filters/{parent.stem}/{name}_vb.jpg", vertical_mb) 
    cv2.imwrite(f"./filters/{parent.stem}/{name}_hb.jpg", horizonal_mb) 
    
    shutil.copyfile(labelpath, f"./filters/{parent.stem}/{name}_vb.txt")
    shutil.copyfile(labelpath, f"./filters/{parent.stem}/{name}_hb.txt")

    # for id, filter in enumerate(filters):
    #     new_img = filter(img)
    #     cv2.imwrite(SRC_PATH + f'filters/{path}_{id}.jpg', new_img)
    #     shutil.copyfile(labelpath, SRC_PATH + f'filters/{path}_{id}.txt')
