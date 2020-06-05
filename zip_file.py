# coding=utf-8
# aistudio的数据上传有每个压缩包不超过10g的限制，因此写一个脚本将一个文件夹下的数据打成不超过10g的包
import zipfile
import os
from tqdm import tqdm
import time

file_dir = "/media/1tDisk/data/processing/rsna/stage_2_test"
zip_dir = "/media/1tDisk/data/processing/rsna/stage_2_test_zip"

num = 1
curr_name = "stage2-test-{}.zip".format(num)
curr_zip = os.path.join(zip_dir, curr_name)
ind = 0

for file in tqdm(os.listdir(file_dir)):

    # print(file, curr_zip)

    f = zipfile.ZipFile(curr_zip, "a", zipfile.ZIP_DEFLATED)
    f.write(os.path.join(file_dir, file), file)
    f.close()
#    os.remove(os.path.join(file_dir, file))

    if os.path.getsize(curr_zip) / 1024 / 1024 / 1024 > 9.7:
        num += 1
        curr_name = "tumor-xz-{}.zip".format(num)
        curr_zip = os.path.join(zip_dir, curr_name)
    if ind == 1024:
        time.sleep(10)
        ind = 0
    ind += 1

    # input("pause")


# 6055
