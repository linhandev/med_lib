import os
import argparse
from multiprocessing import Pool

import nibabel as nib
import numpy as np
import scipy.ndimage

parser = argparse.ArgumentParser()
parser.add_argument("--scan_dir", type=str, default="/home/lin/Desktop/data/aorta/external/nii_raw/")
parser.add_argument("--out_dir", type=str, default="/home/lin/Desktop/data/aorta/external/nii_512/")
args = parser.parse_args()


def to_512(name):

    scanf = nib.load(os.path.join(args.scan_dir, name))
    scan_header = scanf.header
    scan_data = scanf.get_fdata()
    print(scan_data.shape)
    if scan_data.shape[0] != 512:
        scale = 512 / scan_data.shape[0]
        print(scale)
        scan_data = scipy.ndimage.interpolation.zoom(scan_data, (scale, scale, 1), order=3)
    print(scan_data.shape)
    newf = nib.Nifti1Image(scan_data.astype(np.float32), scanf.affine, scan_header)
    nib.save(newf, os.path.join(args.out_dir, name))


if __name__ == "__main__":
    names = os.listdir(args.scan_dir)
    print(names)
    p = Pool(8)
    p.map(to_512, names)
