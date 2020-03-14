# 这个想尝试一下用去预增站的方法加速标注
# 标注的时候在片内画一道竖线，横向做类似区域增长的操作作出一个圆
# vol和lab直接get_fdata之后，片子的脊柱是靠在右侧的，第一个维度是片子的竖向，人的横向; 第二个维度是片子的横向，人的竖向，第三个维度是层

import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import queue

volf = nib.load('/home/lin/Desktop/data/aorta/volume/尹绍文_20200117150142734_0003.nii')
labf = nib.load('/home/lin/Desktop/data/aorta/label/尹绍文_20200117150142734_0003.nii')

vol = volf.get_fdata()
lab = labf.get_fdata()

print(vol.shape)
print(lab.shape)

margin = (10, 60)

for sli_ind in range(lab.shape[2]):
    vols = vol[:, :, sli_ind]
    labs = lab[:, :, sli_ind]

    for line_ind in range(lab.shape[1]):  # 竖向扫描线
        voll = vols[:, line_ind]
        labl = labs[:, line_ind]

        if np.sum(labl) != 0:
            # print(line_ind)
            # print(np.where(line == 1)[0][0])
            seed = np.where(labl == 1)[0][0]
            q = queue.Queue(1024)
            q.put(seed)
            while not q.empty():
                nowp = q.get()
                gops = [nowp - 1, nowp + 1]
                for gop in gops:
                    if( gop >=0 and gop <lab.shape[0] and
                        lab[gop, line_ind, sli_ind] != 1 and
                        abs(voll[gop] - voll[nowp]) < margin[0] and
                        abs(voll[gop] - voll[seed]) < margin[1]):

                        lab[gop, line_ind, sli_ind] = 1
                        q.put(gop)
    # if np.sum(labs) > 0:
    #     plt.imshow(labs)
    #     plt.show()

nlabf = nib.Nifti1Image(lab, np.eye(4))
nib.save(nlabf, 'line_rg.nii')
