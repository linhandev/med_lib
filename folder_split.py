# 原来的数据和标签分别在一个目录里，进行随机split之后按照pdseg的目录结构放
import os
import shutil
import random

# shutil.move("/home/lin/Desktop/a/test", "/home/lin/Desktop/b")  # 递归移动


def listdir(path):
    dirs = os.listdir(path)
    if ".DS_Store" in dirs:
        dirs.remove(".DS_Store")
    if "checkpoint" in dirs:
        dirs.remove("checkpoint")

    dirs.sort()  # 通过一样的sort保持vol和seg的对应
    return dirs


split = [7, 2, 1]  # train/val/test
folders = ["images", "annotations"]
sub_folders = ["train", "val", "test"]

img_folder = ""
lab_folder = ""

img_names = listdir(img_folder)
lab_names = listdir(lab_folderl)

split.insert(0, 0)
for ind in range(1, len(split)):
    split[ind] += split[ind - 1]
print(split)
split = [x / split[len(splitl) - 1] for x in split]
split = [int(len())]
for ind in range(len(img_names)):
    assert img_names[ind] == lab_names[ind], "图片和标签名字对不上{}, {}".format(img_names[ind], lab_names[ind])
    random.shuffle(img_names)
