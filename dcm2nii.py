import nibabel as nib
import numpy as np
import os
from mate.load_input_data import load_input_data
import matplotlib.pyplot as plt

dcm_dir = "/home/lin/Desktop/test/patient/"
nii_dir = "/home/lin/Desktop/test/"
for dcm_name in os.listdir(dcm_dir):
    dcm, info_dict = load_input_data(os.path.join(dcm_dir, dcm_name))
    print(dcm.shape)
    dcm = dcm.swapaxes(0, 2)
    nii = nib.Nifti1Image(dcm, np.eye(4))
    nib.save(nii, os.path.join(nii_dir, dcm_name))
