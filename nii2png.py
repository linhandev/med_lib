# 将 nii 格式的影像转换成png格式的图片
import nibabel as nib
import os
import cv2
import numpy as np


nii_dir = "/home/lin/Desktop/data/aorta/volume"
# nii_dir = "/home/lin/Desktop/data/aorta/label"
png_dir = "/home/lin/Desktop/data/aorta/pngs"

nii_names = os.listdir(nii_dir)
for nii_name in nii_names:
    print(nii_name)
    volf = nib.load(os.path.join(nii_dir, nii_name))
    vol = volf.get_fdata()
    vol = np.rot90(vol)
    vol = np.rot90(vol)
    vol = np.rot90(vol)
    wl, wh = (, )
    vol = vol.clip(-100, 100)
    # vol = (vol + 100) / 200 * 256
    # vol = vol + 100
    print(vol.shape)
    if not os.path.exists(os.path.join(png_dir, nii_name)):
        os.makedirs(os.path.join(png_dir, nii_name))
    for ind in range(vol.shape[2]):
        # file_path = os.path.join(png_dir, "{}-{}.png".format(nii_name, ind))
        file_path = os.path.join(
            png_dir,
            nii_name,
            "{}-{}.png".format(nii_name.rstrip(".nii.gz"), ind),
        )
        slice = vol[:, :, ind]
        cv2.imwrite(file_path, slice)
    # input("here")
