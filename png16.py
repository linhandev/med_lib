import png
import numpy as np
import sys
import os
import pydicom
import matplotlib.pyplot as plt

np.set_printoptions(threshold=sys.maxsize)


dcm_dir = "/home/lin/Desktop/test/patient/"
png_dir = "/home/lin/Desktop/test/png"

for dcm_name in os.listdir(dcm_dir)[:20]:
    if dcm_name.endswith("dcm"):
        print(os.path.join(dcm_dir, dcm_name))
        img = pydicom.dcmread(os.path.join(dcm_dir, dcm_name))
        img = img.pixel_array

        wl, wh = (100, 150.0)
        img = img.astype("float32").clip(wl, wh)
        img = (img - wl) / (wh - wl) * 256
        img = img.astype("uint8")

        # plt.imshow(img)
        # plt.show()

        writer = png.Writer(width=img.shape[1], height=img.shape[0], bitdepth=8, greyscale=True)
        img = img.tolist()

        img_path = os.path.join(png_dir, os.path.basename(dcm_name).replace("dcm", "png"))
        with open(img_path, "wb") as f:
            writer.write(f, img)
