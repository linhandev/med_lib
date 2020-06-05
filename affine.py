import os
import nibabel as nib
import numpy as np

lab_dir = "/home/lin/Desktop/914二院数据/CT/orig/label/"
new_lab_dir = "/home/lin/Desktop/914二院数据/CT/orig/label-affine/"
scan_dir = "/home/lin/Desktop/914二院数据/CT/orig/nii_512/"

names = os.listdir(lab_dir)
for name in names:
    scanf = nib.load(os.path.join(scan_dir, name))
    print(scanf.header)
    scan_header = scanf.header

    label_data = nib.load(os.path.join(lab_dir, name)).get_fdata()

    newf = nib.Nifti1Image(label_data.astype(np.float64), scanf.affine, scan_header)
    nib.save(newf, os.path.join(new_lab_dir, name))
