import os

nii_dir = "/home/lin/Desktop/914二院数据/CT/orig/nii/"
niis = os.listdir(nii_dir)
niis = [n for n in niis if n.endswith("nii")]
# 俞越_20200914224354954.nii
for nii in niis:
    new_name = nii.split("_")
    new_name = new_name[0] + ".nii"
    print(new_name)
    os.rename(os.path.join(nii_dir, nii), os.path.join(nii_dir, new_name))
    # input("here")
