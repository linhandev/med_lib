import numpy as np
import os
import pydicom
import cv2
import sys
import imageio
import matplotlib.pyplot as plt


from PIL import Image

np.set_printoptions(threshold=sys.maxsize)


dcm_dir = "/home/lin/Desktop/test/patient/"
png_dir = "/home/lin/Desktop/test/patient/png"
for dcm_name in os.listdir(dcm_dir)[:20]:
    if dcm_name.endswith("dcm"):
        print(os.path.join(dcm_dir, dcm_name))
        img = pydicom.dcmread(os.path.join(dcm_dir, dcm_name))
        img = img.pixel_array
        # plt.hist(img)
        # plt.show()

        print(img.max(), img.min())

        wl, wh = (200, 1000.0)
        img = img.astype("float32").clip(wl, wh)
        img = (img - wl) / (wh - wl) * 256
        img = img.astype("uint8")

        # img = np.clip(img, , 150)
        # img = (img + 50) / 200 * 255
        # img = img.astype("uint8")

        print(img.max(), img.min())

        img_path = os.path.join(png_dir, os.path.basename(dcm_name).replace("dcm", "png"))

        # imsave(img_path, img)
        # im = Image.fromarray(img)
        # im.save(img_path)
        plt.imshow(img)
        plt.show()
        cv2.imwrite(img_path, img)
        # imageio.imwrite(img_path, img)
