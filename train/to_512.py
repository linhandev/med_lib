import os

import nibabel as nib
import numpy as np
import argparse
import scipy.ndimage

parser = argparse.ArgumentParser()
parser.add_argument(
    "--scan_dir", type=str, default="/home/lin/Desktop/data/aorta/external/nii_raw/"
)
parser.add_argument(
    "--out_dir", type=str, default="/home/lin/Desktop/data/aorta/external/nii_512/"
)


def to_512(scan_dir, out_dir):
    names = os.listdir(args.scan_dir)

    print(names)
    for name in names:
        print("--------")
        scanf = nib.load(os.path.join(scan_dir, name))
        scan_header = scanf.header
        scan_data = scanf.get_fdata()
        print(scan_data.shape)
        if scan_data.shape[0] != 512:
            scale = 512 / scan_data.shape[0]
            print(scale)
            scan_data = scipy.ndimage.interpolation.zoom(
                scan_data, (scale, scale, 1), order=3
            )
        print(scan_data.shape)
        newf = nib.Nifti1Image(scan_data.astype(np.float32), scanf.affine, scan_header)
        nib.save(newf, os.path.join(out_dir, name))


if __name__ == "__main__":
    args = parser.parse_args()
    to_512(args.scan_dir, args.out_dir)
