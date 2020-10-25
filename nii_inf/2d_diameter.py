# 用mesh进行3d重建，之后计算管径
import argparse
import os
import sys
import math

from tqdm import tqdm
import numpy as np
import cv2
import nibabel as nib
import scipy.ndimage
from skimage import filters
import matplotlib.pyplot as plt

np.set_printoptions(threshold=sys.maxsize)


parser = argparse.ArgumentParser()
parser.add_argument("--in_dir", type=str, default="/home/lin/Desktop/git/med/med_lib/nii_inf/seg")
parser.add_argument("--out_dir", type=str, default="./diameter")
args = parser.parse_args()


class Polygon:
    def __init__(self, points, height):
        self.points = points
        self.height = height
        self.center = [0, 0]
        self.diameters = []
        # 计算边缘位置平均数做圆心
        # TODO: 研究用霍夫圆算圆心
        # TODO: 检验圆心是不是真的在圆里面
        for p in self.points:
            self.center[0] += p[0]
            self.center[1] += p[1]
        self.center[0] /= len(self.points)
        self.center[1] /= len(self.points)
        self.center[0] = int(self.center[0])
        self.center[1] = int(self.center[1])

        # print(self.center)

    def ang_sort(self):
        pass

    def plot(self):
        img = np.zeros([512, 512])
        for ind in range(len(self.points)):
            img[self.points[ind][0]][self.points[ind][1]] = 1
        img[self.center[0]][self.center[1]] = 1
        plt.imshow(img)
        plt.show()

    def cal_diameters(self, ang_range=[0, np.pi], split=30, pixdim=1):
        """用类似二分的方法，平行线夹计算管径.

        y - y0 + d = k ( x - x0 )：d是这根线在y轴上移动的距离
        取x=0(a), x=1(b) a，b两点，通过判断a，b，points上的各个点p是不是都向同一个方向转，判断直线是不是已经移出了多边形

        Parameters
        ----------
        ang_range : list
            直线和x轴角度的范围.
        split : int
            在这个范围内，平均测量多少个方向.
        pixdim : float
            片子的pixdim，从像素换算到实际的mm.

        Returns
        -------
        list
            ang_range 角度范围内，split 等分个方向上，平行线夹的管径是多少mm.

        """

        def is_right(a, b, c):
            a = np.array((b[0] - a[0], b[1] - a[1]))
            b = np.array((c[0] - b[0], c[1] - b[1]))
            res = np.cross(a, b)
            if res >= 0:
                return True
            return False

        diameters = []
        center = self.center
        for alpha in np.arange(ang_range[0], ang_range[1], (ang_range[1] - ang_range[0]) / split):
            if alpha == np.pi / 2:
                continue
            k = math.tan(alpha)

            def binary_search(step):
                d = 0
                prev_out = False
                while True:
                    # print(d)
                    ya = center[1] - d + k * (0 - center[0])  # (0,ya)
                    yb = center[1] - d + k * (1 - center[0])  # (1,yb)

                    dir = is_right((0, ya), (1, yb), self.points[0])
                    same_dir = True
                    for p in self.points:
                        if dir != is_right((0, ya), (1, yb), p):
                            same_dir = False
                            break
                    # print(same_dir)
                    if same_dir:
                        if not prev_out:
                            step /= 2
                        d -= step
                        prev_out = True
                    else:
                        d += step
                        prev_out = False
                    if abs(step) < 0.1:
                        break
                return d

            diameters.append((binary_search(100) - binary_search(-100)) * np.abs(np.cos(alpha)) * pixdim)
        self.diameters = diameters
        return diameters
        # print(diameters)


def dist(a, b):
    h = a.height - b.height
    ca = a.center
    cb = b.center
    return ((ca[0] - cb[0]) ** 2 + (ca[1] - cb[1]) ** 2 + h ** 2) ** 0.5


# print(dist(Polygon([[0, 0]], 0, [0, 0]), Polygon([[0, 0]], 1, [1, 2])))


def blood_sort(polygons):
    # TODO: 主动脉弓最上面那几片排序不对，可以研究怎么去掉他

    if len(polygons) == 0:
        print("Error, got None points")
        return

    # 1. 计算最低的片层，认为是降主动脉最下面一片，排序的开始
    ordered = []
    min_height = polygons[0].height
    min_ind = 0
    for idx, p in enumerate(polygons):
        if p.height < min_height:
            min_height = p
            min_ind = idx
    # 2. 一直找无序的list中和当前最后一个距离最近的作为下一个
    ordered.append(polygons[min_ind])
    del polygons[min_ind]

    while len(polygons) != 0:
        min_dist = dist(ordered[-1], polygons[0])
        min_ind = 0
        for idx, p in enumerate(polygons):
            d = dist(ordered[-1], p)
            if d < min_dist:
                min_dist = d
                min_ind = idx
        ordered.append(polygons[min_ind])
        del polygons[min_ind]
    return ordered


def cal_diameter(seg_path):
    """计算seg_path这个nii分割文件的所有管径，返回.

    过程：
    1.  按照血流反向，获取所有圆
    1.1 按照高度分片层，层内找连通块，可能一块可能两块，计算层中心
    1.2 从最下面的中心开始，找最近的没入序列的中心，对中心按照血流方向反向排序

    2. 用平行线夹计算血管管径
    2.1

    Parameters
    ----------
    seg_path : str
        这个人的分割文件路径.

    Returns
    -------
    type
        Description of returned object.

    """
    segf = nib.load(seg_path)
    seg_data = segf.get_fdata()
    pixdim = segf.header["pixdim"][1]
    seg_data[seg_data > 0.9] = 1
    seg_data = seg_data.astype("uint8")
    print(seg_data.shape)
    polygons = []
    for height in range(seg_data.shape[2]):
        label = seg_data[:, :, height]
        label = filters.roberts(label)
        vol, num = scipy.ndimage.label(label, np.ones([3, 3]))
        for label_idx in range(1, num + 1):
            xs, ys = np.where(vol == label_idx)
            points = []
            for x, y in zip(xs, ys):
                points.append([x, y])
            polygons.append(Polygon(points, height))
    polygons = blood_sort(polygons)
    # for p in polygons:
    #     p.plot()
    for p in tqdm(polygons):
        p.cal_diameters(pixdim=pixdim)
    print(os.path.join(args.out_dir, seg_path.split("/")[-1]))
    f = open(os.path.join(args.out_dir, seg_path.split("/")[-1].rstrip(".gz").rstrip(".nii")) + ".csv", "w")
    for p in polygons:
        print(p.height, end=",", file=f)
        for d in p.diameters:
            print(d, end=",", file=f)
        print(end="\n", file=f)
    f.close()

    # input("here")


if __name__ == "__main__":
    names = os.listdir(args.in_dir)
    [os.path.join(args.in_dir, name) for name in names]
    for name in names:
        cal_diameter(os.path.join(args.in_dir, name))
