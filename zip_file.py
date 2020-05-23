# aistudio的数据上传有每个压缩包不超过10g的限制，因此写一个脚本将一个文件夹下的数据打成不超过10g的包
import zipfile
import os
from tqdm import tqdm

file_dir = "/home/aistudio/data/zprep"
zip_dir = "/home/aistudio/data/prep_zip"

num = 1
curr_name = "tumor-xz-{}.zip".format(num)
curr_zip = os.path.join(zip_dir, curr_name)

for file in tqdm(os.listdir(file_dir)):

    # print(file, curr_zip)

    f = zipfile.ZipFile(curr_zip, "a", zipfile.ZIP_DEFLATED)
    f.write(os.path.join(file_dir, file), file)
    f.close()
    os.remove(os.path.join(file_dir, file))

    if os.path.getsize(curr_zip) / 1024 / 1024 / 1024 > 9.7:
        num += 1
        curr_name = "tumor-xz-{}.zip".format(num)
        curr_zip = os.path.join(zip_dir, curr_name)

    # input("pause")


# 6055
