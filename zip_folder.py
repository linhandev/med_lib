# aistudio的数据上传有每个压缩包不超过10g的限制，因此写一个脚本将一个文件夹下的数据打成不超过10g的包

import zipfile
import os
from tqdm import tqdm

file_dir = "/home/aistudio/data/preprocess"
zip_dir = "/home/aistudio/data/prep_zip"

num = 1
for file in os.listdir(file_dir):
    curr_name = "liver-{}.zip".format(num)
    curr_zip = os.path.join(zip_dir, curr_name)

    print(file, curr_zip)

    f = zipfile.ZipFile(curr_zip, "a", zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in tqdm(
        os.walk(os.path.join(file_dir, file))
    ):
        for filename in filenames:
            print(os.path.join(dirpath, filename))
            f.write(
                os.path.join(dirpath, filename), os.path.join(file, filename)
            )
    f.close()
    os.removedirs(dirpath)
    # f.write(os.path.join(file_dir, file), file)
    if os.path.getsize(curr_zip) / 1024 / 1024 / 1024 > 9.7:
        num += 1


# f = zipfile.ZipFile("./test.zip", "w", zipfile.ZIP_DEFLATED)
# f.write("./cat.png")
# print(os.path.getsize("./test.zip") / 1024 / 1024 / 1024)
# f.close()
