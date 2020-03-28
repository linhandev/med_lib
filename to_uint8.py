# 这段代码把一个路径下所有的nii转成uint8格式的

import nibabel as nib
import numpy as np
import os

nii_dir = '/home/lin/Desktop/data/lits/submit'
uint8_dir = '/home/lin/Desktop/data/lits/uint8'
names = os.listdir(nii_dir)

for name in names:
	print(name)
	path = os.path.join(nii_dir, name)
	volf = nib.load(path)
	vol = volf.get_fdata()
	print(vol.shape)
	print(vol.dtype)

	vol = vol.astype(np.int8)
	print(vol.dtype)
	newf = nib.Nifti1Image(vol, np.eye(4))
	nib.save(newf, os.path.join(uint8_dir, name) )
	# input("pause")
