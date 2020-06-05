# 将 nii 转成一定的分辨率
# 将 nii 格式的影像转换成png格式的图片
import nibabel as nib
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
import scipy
import scipy.ndimage

parser = argparse.ArgumentParser()
parser.add_argument("--in_dir", type=str, default="/home/lin/Desktop/914二院数据/CT/orig/nii_raw/")
parser.add_argument("--out_dir", type=str, default="/home/lin/Desktop/914二院数据/CT/orig/nii_512/")
args = parser.parse_args()


in_dir = args.in_dir
out_dir = args.out_dir

nii_names = os.listdir(in_dir)
nii_names = [n for n in nii_names if n.endswith("gz") or n.endswith("nii")]
for nii_name in nii_names:
    print(nii_name)
    volf = nib.load(os.path.join(in_dir, nii_name))
    vol = volf.get_fdata()
    header = volf.header.copy()

    if vol.shape[0] == 1024:
        vol = scipy.ndimage.interpolation.zoom(vol, (0.5, 0.5, 1), order=3)
        d = header["pixdim"]
        header["pixdim"] = [-1, d[1] * 2, d[2] * 2, d[3], 0, 0, 0, 0]
        d = header["dim"]
        header["dim"][1] = header["dim"][2] = 512

    print("--------------------")
    print(header)
    print(vol.shape)

    newf = nib.Nifti1Image(vol.astype(np.float64), volf.affine, header)
    nib.save(newf, os.path.join(args.out_dir, nii_name))
    # input("here")
