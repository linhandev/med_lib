制作paddleseg格式的训练集
python prep_dateset.py
python folder_split.py

lits

python prep_dateset.py --scan_dir /home/lin/Desktop/data/lits/nii/scan --label_dir /home/lin/Desktop/data/lits/nii/label --scan_img_dir /home/lin/Desktop/data/lits/img/scan --label_img_dir /home/lin/Desktop/data/lits/img/label

python folder_split.py --base_dir /home/lin/Desktop/data/lits/dataset --img_folder /home/lin/Desktop/data/lits/img/scan --lab_folder /home/lin/Desktop/data/lits/img/label
