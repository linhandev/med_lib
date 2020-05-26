# 多种格式的医学影像数据读取和保存，数据和头文件信息
# 信息包括：大小，体素间距
import SimpleITK as sitk
import matplotlib.pyplot as plt
import os
import nibabel as nib
import numpy as np

img_dir = "/home/lin/Desktop/data/sliver/scan"
paths = os.listdir(img_dir)
print(paths)

for path in paths:
    if path.find("mhd") >= 0:
        data = sitk.ReadImage(os.path.join(img_dir, path))
        spacing = data.GetSpacing()
        print(spacing)
        scan = sitk.GetArrayFromImage(data)
        scan = scan.swapaxes(0, 2)
        scan = np.rot90(scan)
        scan = np.rot90(scan)
        print(scan.shape)

        newf = nib.Nifti1Image(scan, np.eye(4))
        nib.save(
            newf,
            os.path.join("/home/lin/Desktop/data/sliver/nii_vol/", "sl07-" + path.rstrip("mdh").lstrip("liver-orig") + "nii"),
        )

        # input("pause")
