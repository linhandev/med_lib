import nibabel as nib
import matplotlib.pyplot as plt
import cv2
import numpy as np

segf = nib.load("/home/lin/Desktop/data/lits/nii/label/volume-127.nii.gz")
data = segf.get_fdata()
print(data.shape)
slice = data[:, :, 650]
plt.imshow(slice, cmap="gray")
plt.show()

slice[slice > 0.9] = 1
slice = slice.astype("uint8")
slice = slice * 255
edges = cv2.Canny(slice, 1, 100)
plt.imshow(edges, cmap="gray")
plt.show()


print(np.where(edges != 255))

temp = edges.copy()
for idx in range(1, edges.shape[0] - 2):
    for idy in range(1, edges.shape[1] - 2):
        if edges[idx][idy] == 255:

            temp[idx + 1][idy + 1] = 255
            temp[idx + 1][idy - 1] = 255
            temp[idx - 1][idy + 1] = 255
            temp[idx - 1][idy - 1] = 255

            temp[idx + 2][idy + 2] = 255
            temp[idx + 2][idy - 2] = 255
            temp[idx - 2][idy + 2] = 255
            temp[idx - 2][idy - 2] = 255

temp = 255 - temp
temp = temp.clip(32, 235)
map = cv2.applyColorMap(temp, cv2.COLORMAP_JET)
plt.imshow(map)
plt.show()

bold = edges.copy()
for idx in range(1, edges.shape[0] - 2):
    for idy in range(1, edges.shape[1] - 2):
        if edges[idx][idy] == 255:

            bold[idx + 1][idy + 1] = 255
            bold[idx + 1][idy - 1] = 255
            bold[idx - 1][idy + 1] = 255
            bold[idx - 1][idy - 1] = 255

            bold[idx + 2][idy + 2] = 255
            bold[idx + 2][idy - 2] = 255
            bold[idx - 2][idy + 2] = 255
            bold[idx - 2][idy - 2] = 255

            bold[idx + 3][idy + 3] = 255
            bold[idx + 3][idy - 3] = 255
            bold[idx - 3][idy + 3] = 255
            bold[idx - 3][idy - 3] = 255

            bold[idx + 4][idy + 4] = 255
            bold[idx + 4][idy - 4] = 255
            bold[idx - 4][idy + 4] = 255
            bold[idx - 4][idy - 4] = 255

            bold[idx + 5][idy + 5] = 255
            bold[idx + 5][idy - 5] = 255
            bold[idx - 5][idy + 5] = 255
            bold[idx - 5][idy - 5] = 255

            bold[idx + 6][idy + 6] = 255
            bold[idx + 6][idy - 6] = 255
            bold[idx - 6][idy + 6] = 255
            bold[idx - 6][idy - 6] = 255
plt.imshow(bold)
plt.show()


kernel = np.ones((15, 15), np.float32) / 15 ** 2
smoothed = cv2.filter2D(bold, -1, kernel)
smoothed = cv2.filter2D(smoothed, -1, kernel)
smoothed = cv2.filter2D(smoothed, -1, kernel)
smoothed = cv2.filter2D(smoothed, -1, kernel)
# smoothed = cv2.filter2D(smoothed, -1, kernel)
# smoothed = cv2.filter2D(smoothed, -1, kernel)


plt.imshow(smoothed)
plt.show()

smoothed = 255 - smoothed
smoothed = smoothed.clip(0, 240)
# map = cv2.applyColorMap(np.ones([255, 255], dtype="uint8") * 255, cv2.COLORMAP_JET)
map = cv2.applyColorMap(smoothed, cv2.COLORMAP_JET)
plt.imshow(map)
plt.show()
