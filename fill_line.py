# 希望自动通过扫描线填充边缘标画过的seg区
# TODO: 遇到的问题是左右两个边缘，向下两个动脉还有边缘和中间部分组合的问题


import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib

labf = nib.load('/home/lin/Desktop/data/aorta/label/zsz_0002.nii')
lab = labf.get_fdata()
filled = np.zeros(lab.shape)

print(lab.shape)

# slice = lab[0:300,:,34] # 35
# plt.imshow(slice)
# plt.show()
#
#
# slice = lab[0:300,:,35] # 36
# plt.imshow(slice)
# plt.show()

# 第 2 个维度是层数，从0开始，和itk里面下表是 i 对应 i + 1
# 片内是 itk 显示的片子顺时针转90度
# 第 0 个维度在数组中是上到下，在itk中是左到右
# 第 1 个维度在数组中是左到右，在itk中是上到下

for sli_ind in range(lab.shape[2]):
    for line_ind in range(lab.shape[0]):  # 这个下标是竖向的下标， 走横向的
        line = lab[line_ind, :, sli_ind]
        if np.sum(line) == 0:
            continue
        inside = False
        for i in range(1, lab.shape[1] - 1):
            if inside or line[i - 1] == 1:
                filled[line_ind, i - 1, sli_ind] = 1
            if line[i - 1] == line[i]:
                continue
            if not inside and (line[i - 1] == 1 and line[i] == 0): # 本来不在里面，i像素是一个开始像素
                inside = True
                continue
            if inside and (line[i - 1] == 1 and line[i] == 0): # 本来在里面，i像素是一个终止像素
                inside = False



filledf = nib.Nifti1Image(filled, np.eye(4))
nib.save(filledf, 'filled.nii')
