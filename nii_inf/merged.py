import os
from multiprocessing import Pool
import sys

import nibabel as nib
import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
from tqdm import tqdm
import skimage.measure
import scipy.ndimage

from util.util import filter_polygon, sort_line, Polygon


parser = argparse.ArgumentParser()
parser.add_argument("--nii_dir", type=str, default="scan")
parser.add_argument("--png_dir", type=str, default="img")
parser.add_argument("--seg_dir", type=str, default="seg")


def to_png(nii_dir, png_dir):
    """将 nii_dir下所有的nii扫描转换成png，一组扫描放到一个文件夹.

    Parameters
    ----------
    nii_dir : type
        Description of parameter `nii_dir`.
    png_dir : type
        Description of parameter `png_dir`.

    Returns
    -------
    type
        Description of returned object.

    """

    nii_names = os.listdir(nii_dir)
    pbar = tqdm(nii_names)
    for nii_name in pbar:
        pbar.set_description("Converting: ", nii_name)

        volf = nib.load(os.path.join(nii_dir, nii_name))
        vol = volf.get_fdata()
        vol = np.rot90(vol)

        wl, wh = (-200.0, 200.0)
        vol = vol.astype("float32").clip(wl, wh)
        vol = (vol - wl) / (wh - wl) * 256
        vol = vol.astype("uint8")
        patient_name = nii_name.rstrip(".gz").rstrip(".nii")
        if not os.path.exists(os.path.join(png_dir, patient_name)):
            os.makedirs(os.path.join(png_dir, patient_name))
        for ind in range(1, vol.shape[2] - 1):
            file_path = os.path.join(
                png_dir,
                patient_name,
                "{}-{}.png".format(patient_name, ind),
            )
            slice = vol[:, :, ind - 1 : ind + 2]
            cv2.imwrite(file_path, slice)


def to_nii(png_dir, seg_dir, scan_dir):
    img_names = os.listdir(png_dir)
    patient_names = []

    for n in img_names:
        if not n.endswith("mask.png"):
            continue
        n = n.split("-")
        if n[0] not in patient_names:
            patient_names.append(n[0])
    print(patient_names)

    all_imgs = os.listdir(png_dir)
    for patient in patient_names:
        img_names = [
            n for n in all_imgs if n.startswith(patient) and n.endswith("mask.png")
        ]
        img_names.sort(key=lambda n: int(n.split("-")[1].split("_")[0]))
        print(img_names)
        print(len(img_names))

        img_data = np.zeros([512, 512, len(img_names)])
        print(img_data.shape)

        for img_name in img_names:
            img = cv2.imread(os.path.join(png_dir, img_name))
            ind = int(img_name.split("-")[1].split("_")[0])
            img = img.swapaxes(0, 1)
            img = img[:, ::-1, 0]
            img_data[:, :, ind] = img
        # img_data = filter_largest_volume(img_data)

        scanf = nib.load(os.path.join(scan_dir, patient + ".nii.gz"))
        header = scanf.header
        print(header)
        newf = nib.Nifti1Image(img_data.astype(np.float64), scanf.affine, header)
        nib.save(newf, os.path.join(seg_dir, patient + ".nii.gz"))


def cal_diameter(seg_dir):
    vol_names = os.listdir(seg_dir)
    vol_names = set(vol_names)

    done = os.listdir("/home/lin/Desktop/git/med/med_lib/nii_inf/diameter")
    done = [n[:-4] for n in done]
    done = set(done)

    print(done)
    print(len(done))
    print(len(vol_names))
    vol_names = vol_names - done
    print(vol_names)
    print(len(vol_names))
    input("here")
    with Pool(7) as p:
        print(p.map(diameter_process, vol_names))


def diameter_process(vol_name):
    # 1. 获取需要测量的标签数据，插值成1024分辨率提升精度
    volf = nib.load(os.path.join(args.seg_dir, vol_name))
    pixdim = volf.header["pixdim"]
    print(pixdim)
    vol = volf.get_fdata()
    print(vol.shape)
    verts, faces, normals, values = skimage.measure.marching_cubes(vol)

    # 3. 获取测量路径，在血管壁上取一条线的点
    # 3.1 查所有不同的高度，作为一个片曾
    heights = []
    for v in verts:
        if v[2] not in heights:
            heights.append(v[2])
    print("heights", heights)

    slices = [[] for _ in range(len(heights))]
    for ind, h in enumerate(heights):
        for v in verts:
            if v[2] == h:
                slices[ind].append(v)

    # 3.2 算所有片曾的圆心
    centers = []
    polygons = []
    for ind in range(len(heights)):
        res = filter_polygon(slices[ind], "all", 15)
        for poly in res:
            if len(poly) < 3:
                continue
            # print(poly)
            polygons.append(Polygon(poly))
    polygons = sort_line(polygons)
    print("starting to cal {}".format(vol_name))
    diameters = []
    f = open("./diameter/{}.csv".format(vol_name), "w")
    for poly in tqdm(polygons):
        print(len(poly.points))
        if len(poly.points) < 10:
            print(len(poly.points), "skipping")
            continue
        diameters.append(poly.cal_diameter(split=20, step=0.3, pixdim=pixdim[1]))
        # print(diameters[-1])
        for d in diameters[-1]:
            print(d, end=",", file=f)
        print("\n", end="", file=f)
        # poly.plot_2d()
        f.flush()

    f.close()
    print(diameters)


args = parser.parse_args()
if __name__ == "__main__":
    dirname, _ = os.path.split(os.path.abspath(sys.argv[0]))

    # 1. 把所有图片转成png
    # to_png(args.nii_dir, args.png_dir)
    # 2. 对所有的文件夹进行推理，结果存到nii放到seg文件夹
    # folders = os.listdir(args.png_dir)
    # for folder in folders:
    #     input_dir = os.path.join(dirname, args.png_dir, folder)
    #     print(input_dir)
    #     os.system("python infer.py --conf=model/deploy.yaml --input_dir {} --ext png".format(input_dir))
    #     to_nii(input_dir, args.seg_dir, args.nii_dir)
    # 3.测管径
    cal_diameter(args.seg_dir)
