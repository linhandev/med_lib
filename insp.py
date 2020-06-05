import os

import matplotlib.pyplot as plt
import argparse
import cv2
import numpy as np


np.set_printoptions(threshold=np.inf)

parser = argparse.ArgumentParser()
parser.add_argument("--scan_dir", type=str, default="/home/lin/Desktop/data/aorta/dataset/images/train")
parser.add_argument("--label_dir", type=str, default="/home/lin/Desktop/data/aorta/dataset/annotations/train")
args = parser.parse_args()


# print(os.listdir(args.label_dir))
for name in os.listdir(args.label_dir):
    print(name)
    scan = cv2.imread(os.path.join(args.scan_dir, name))
    label = cv2.imread(os.path.join(args.label_dir, name))
    label = label * 255
    plt.figure()
    plt.subplot(1, 2, 1)
    plt.imshow(scan[:, :, 1])
    plt.subplot(1, 2, 2)
    plt.imshow(label)
    plt.show()
