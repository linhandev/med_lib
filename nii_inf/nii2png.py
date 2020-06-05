# 将 nii 格式的影像转换成png格式的图片
import nibabel as nib
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--nii_dir", type=str, default="./scan")
parser.add_argument("--png_dir", type=str, default="./img")
args = parser.parse_args()


nii_dir = args.nii_dir
png_dir = args.png_dir

nii_names = os.listdir(nii_dir)
for nii_name in nii_names:
    print(nii_name)
    volf = nib.load(os.path.join(nii_dir, nii_name))
    vol = volf.get_fdata()
    vol = np.rot90(vol)
    # vol = np.rot90(vol)
    # vol = np.rot90(vol)
    wl, wh = (-200.0, 200.0)
    vol = vol.astype("float32").clip(wl, wh)
    print(vol.max())
    vol = (vol - wl) / (wh - wl) * 256
    print(vol.shape)
    vol = vol.astype("uint8")
    # if not os.path.exists(os.path.join(png_dir, nii_name)):
    #     os.makedirs(os.path.join(png_dir, nii_name))
    for ind in range(vol.shape[2]):
        # plt.imshow(vol[:, :, ind])
        # plt.show()
        # file_path = os.path.join(png_dir, "{}-{}.png".format(nii_name, ind))
        file_path = os.path.join(
            png_dir,
            # nii_name,
            "{}-{}.png".format(nii_name.rstrip(".nii.gz"), ind),
        )
        slice = vol[:, :, ind]
        # plt.imshow(slice)
        # plt.show()
        cv2.imwrite(file_path, slice)
