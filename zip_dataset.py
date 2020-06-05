# coding=utf-8
# 将一个目录下的所有文件和文件夹按照原来的文件结构打包，每个包不超过10g

import zipfile
import os
from tqdm import tqdm

dataset_dir = "/media/1tDisk/data/processing/siim"
zip_dir = "/media/1tDisk/data/processing/siim_zip"
dataset_name = dataset_dir.split("/")[-1]
# print(dataset_name)

zip_num = 1
curr_name = "{}-{}.zip".format(dataset_name, zip_num)
curr_zip_path = os.path.join(zip_dir, curr_name)
f = zipfile.ZipFile(curr_zip_path, "a", zipfile.ZIP_DEFLATED)

files_list = []
list_size = 0
zip_tot_size = 9.5 * 1024 * 10
zip_left_size = zip_tot_size
# 9.7 * 1024 * 1024 * 1024


for dirpath, dirnames, filenames in tqdm(os.walk(os.path.join(dataset_dir))):
    for filename in filenames:
        print(dataset_name, dirpath[len(dataset_dir) :], filename)
        files_list.append(
            [
                os.path.join(dirpath, filename),
                os.path.join(
                    dataset_name, dirpath[len(dataset_dir) :], filename
                ),
            ]
        )
        list_size += os.path.getsize(os.path.join(dirpath, filename))
        if list_size >= zip_left_size * 1.1:  # 如果当前列表中未压缩文件的大小大于 1.1 倍zip包能装的大小
            input("here")
            print(files_list)
            print("Writting {} file".format(len(files_list)))
            # 将列表里所有的文件写入zip
            for pair in files_list:
                f.write(pair[0], pair[1])
            files_list = []
            list_size = 0

            curr_size = os.path.getsize(curr_zip_path)
            print("curr size is: {} M".format(curr_size / 1024 ** 2))

            if curr_size >= zip_tot_size:
                f.close()
                zip_num += 1
                curr_name = "{}-{}.zip".format(dataset_name, zip_num)
                curr_zip_path = os.path.join(zip_dir, curr_name)
                f = zipfile.ZipFile(curr_zip_path, "a", zipfile.ZIP_DEFLATED)
                print("+++ opening new zip: {}  +++".format(curr_name))
                zip_left_space = zip_tot_size
            else:
                zip_left_space = zip_tot_size - curr_size

if len(files_list) != 0:
    for pair in files_list:
        f.write(pair[0], pair[1])
    curr_size = os.path.getsize(curr_zip_path)
    files_list = []
    f.close()


# f.write(
#     os.path.join(dirpath, filename),
#     os.path.join(dirpath[len(dataset_dir) :], filename),
# )
