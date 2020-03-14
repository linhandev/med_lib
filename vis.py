# 把标签和数据都打出来，检查两个数据对的上
import nibabel as nib
import numpy
import os
from mate.load_input_data import load_input_data
import matplotlib.pyplot as plt
vol_dir = '/home/lin/Desktop/data/aorta/volume/'
lab_dir = '/home/lin/Desktop/data/aorta/flood/'

for vol_name in os.listdir(vol_dir):
    vol, info_dict = load_input_data(os.path.join(vol_dir, vol_name))
    labf = nib.load(os.path.join(lab_dir, vol_name + '.nii'))
    lab = labf.get_fdata()
    print(vol.shape)
    print(lab.shape)
    vol = vol.swapaxes(0,2)
    for sli_ind in range(vol.shape[2]):
        plt.imshow(vol[:, :, sli_ind])
        plt.show()

        plt.imshow(lab[:, :, sli_ind])
        plt.show()
