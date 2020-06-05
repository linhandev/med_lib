# 用mesh进行3d重建，之后计算管径
import argparse
import os

import skimage.measure
import scipy.ndimage
import numpy as np
import nibabel as nib
import trimesh
from util import filter_polygon, sort_line, Polygon
from tqdm import tqdm


parser = argparse.ArgumentParser()
parser.add_argument("--in_dir", type=str, default="/home/lin/Desktop/test/mesh/")
parser.add_argument("--out_dir", type=str, default="./img")
args = parser.parse_args()


vol_names = os.listdir(args.in_dir)
for vol_name in vol_names:
    # 1. 获取需要测量的标签数据，插值成1024分辨率提升精度
    volf = nib.load(os.path.join(args.in_dir, vol_name))
    pixdim = volf.header["pixdim"]
    print(pixdim)
    vol = volf.get_fdata()
    print(vol.shape)
    # if vol.shape[0] < 1024:
    #     vol = scipy.ndimage.interpolation.zoom(vol, (2, 2, 1), order=3)
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
            polygons.append(Polygon(poly))

    polygons = sort_line(polygons)
    print(polygons[0].height)
    input("here")
    diameters = []
    for poly in tqdm(polygons):
        diameters.append(poly.cal_diameter())
    print(diameters)
