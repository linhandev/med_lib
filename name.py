import os
from pypinyin import pinyin, Style



def to_pinyin(name):
    new_name = ""
    for ch in name:
        if u"\u4e00" <= ch <= u"\u9fff":
            new_name += pinyin(ch, style=Style.NORMAL)[0][0]
        else:
            new_name += ch
    return new_name

names = os.listdir("/home/lin/Desktop/914二院数据/CT/orig/nii/")
f=open("names.csv","w")
for name in names:
    if name.endswith("nii"):
        print(name+","+to_pinyin(name), file=f)
f.close()
