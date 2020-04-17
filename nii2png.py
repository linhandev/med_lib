# 将 nii 格式的影像转换成png格式的图片
import nibabel as nib
import os
from lib.threshold_function_module import windowlize_image
import cv2
import numpy as np

nii_dir = '/home/lin/Desktop/20_ncov_scan'
png_dir = '/home/lin/Desktop/nconv_pngs'

nii_names = os.listdir(nii_dir)
for nii_name in nii_names:
	print(nii_name)
	volf = nib.load(os.path.join(nii_dir, nii_name))
	vol = volf.get_fdata()
	vol = np.rot90(vol)

	print(vol.shape)
	if not os.path.exists(os.path.join(png_dir, nii_name)):
		os.makedirs( os.path.join(png_dir, nii_name) )
	for ind in range(vol.shape[2]):
		# file_path = os.path.join(png_dir, "{}-{}.png".format(nii_name, ind))
		file_path = os.path.join(png_dir, nii_name, "{}.png".format(ind))
		cv2.imwrite(file_path, vol[:,:,ind])
	# input("here")
