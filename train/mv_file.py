import os
import shutil


def mv(curr, dest):
    print(os.path.join(dest.rstrip(dest.split("/")[-1])))
    if not os.path.exists(os.path.join(dest.rstrip(dest.split("/")[-1]))):
        os.makedirs(os.path.join(dest.rstrip(dest.split("/")[-1])))
    os.rename(curr, dest)
    # shutil.move(curr, dest)
    # os.replace(curr, dest)


mv("/home/lin/Desktop/testf", "/home/lin/Desktop/test/aaa")
