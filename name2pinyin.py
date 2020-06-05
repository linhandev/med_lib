from pypinyin import pinyin, Style
import pydicom
import numpy as np
import os
from util import to_pinyin

base_dir = "/home/lin/Desktop/914二院数据/CT/orig/label"
# print(pinyin("中心", style=Style.NORMAL))

for root, dirs, files in os.walk(base_dir, topdown=False):
    for file in files:
        print(file)
        os.rename(
            os.path.join(root, file),
            os.path.join(root, to_pinyin(file, nonum=True)),
        )
    for dir in dirs:
        print(dir)
        os.rename(
            os.path.join(root, dir),
            os.path.join(root, to_pinyin(dir, nonum=True)),
        )
