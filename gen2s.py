# 生成一样大小的 2

import nibabel as nib
import numpy as np
import os

nii_dir = '/home/lin/Desktop/data/lits/submit'
uint8_dir = '/home/lin/Desktop/data/lits/2s'
names = os.listdir(nii_dir)

for name in names:
	print(name)
	path = os.path.join(nii_dir, name)
	volf = nib.load(path)
	vol = volf.get_fdata()
	print(vol.shape)
	print(vol.dtype)

	vol = 2 * np.ones(vol.shape, dtype=np.uint8)
	print(vol.dtype)
	newf = nib.Nifti1Image(vol, np.eye(4))
	nib.save(newf, os.path.join(uint8_dir, name) )
