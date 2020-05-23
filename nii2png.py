# 将 nii 格式的影像转换成png格式的图片
import nibabel as nib
import os
from lib.threshold_function_module import windowlize_image
import cv2
import numpy as np
import skimage.color


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
    vol = windowlize_image(vol, 1500, -500)  # ww wc
    # vol = vol.clip(-100, 100)
    # vol = (vol + 100) / 200 * 256
    # vol = vol + 100
    print(vol.shape)
    if not os.path.exists(os.path.join(png_dir, nii_name)):
        os.makedirs(os.path.join(png_dir, nii_name))
    for ind in range(vol.shape[2]):
        # file_path = os.path.join(png_dir, "{}-{}.png".format(nii_name, ind))
        file_path = os.path.join(png_dir, nii_name, "{}-{}.png".format(nii_name.rstrip(".nii.gz"), ind))
        slice = vol[:, :, ind]
        # slice = skimage.color.gray2rgb(slice)
        cv2.imwrite(file_path, slice)
    # input("here")
