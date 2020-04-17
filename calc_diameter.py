# 计算一个 nii 格式的片子中，每一片内前景的直径
import nibabel as nib
import os
import numpy as np
import math
import matplotlib.pyplot as plt


def cal_diameter(slice, num=10, ang_range=(-np.pi, np.pi), front_num=1, pixdim=1):
	'''计算一个二维平面内 1 的直径
	slice：2d的np array，第一个维度叫x，第二个叫y
	num：将360度分成num份，每一份算一个直径

	return：一个num长的list，每一个数是一个直径
	'''
	if np.sum(slice) == 0:
		return [0]
	# 1. 计算x,y坐标的范围，求中心点坐标
	front_ind = np.where(slice == 1)
	ind_range = [(arr.min(), arr.max())  for arr in front_ind]
	center_point = [ int( (ind[1]-ind[0])/2 ) + ind[0] for ind in ind_range]
	print("center point is ", center_point)

	# 2. 过中心点做多个角度的线，求其和边缘的交点，算两点距离做直径
	xmid = center_point[0]
	ymid = center_point[1]
	diameters = []
	for k in np.arange(ang_range[0], ang_range[1], 2 * np.pi / num):
		# print("------------------")
		# print(k)

		k = math.tan(k)
		line_x = []
		line_y = []

		# print("k is ", k)

		for x in range(ind_range[0][0], ind_range[0][1]+1):
			y =  k * (x - xmid) + ymid + 0.5
			# print(x, y)
			# input("pause")
			if y >= ind_range[1][0] and y <= ind_range[1][1] and slice[x][int(y)] == front_num:
				line_x.append(x)
				line_y.append(int(y) )
		for y in range(ind_range[1][0], ind_range[1][1]+1):
			x = (y - ymid) / k + xmid + 0.5
			# print(x,y)
			if x >= ind_range[0][0] and x <= ind_range[0][1] and slice[int(x)][y] == front_num:
				line_x.append(int(x) )
				line_y.append(y)
		# print(line_x, line_y)
		if len(line_x) == 0:
			print("no point found")
		line_x = np.array(line_x)
		line_y = np.array(line_y)
		lenx = line_x.max() - line_x.min()
		leny = line_y.max() - line_y.min()
		diameters.append(math.sqrt(lenx**2 + leny**2) * pixdim)

	return diameters


lab_dir = '/home/lin/Desktop/data/aorta/lab_inf/'

for labn in os.listdir(lab_dir):
	pass

labn = 'CCL_0002.nii.gz'
labf = nib.load(os.path.join(lab_dir, labn))
assert labf.header['pixdim'][1] == labf.header['pixdim'][2], "x,y 分辨率不相等{}".format(labf.header['pixdim'])
print(labn)
lab = labf.get_fdata()
for ind in range(lab.shape[2]):
	print(cal_diameter(lab[:,:,ind], 20, labf.header['pixdim'][1]))
	plt.imshow(lab[:,:,ind])
	plt.show()
	# input("pause")
