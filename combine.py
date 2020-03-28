# 将两个分割的结果合在一起
import nibabel as nib
import os
from tqdm import tqdm
import numpy as np
import threading

liver_dir = '/home/lin/Desktop/data/lits/liver_seg'
tumor_dir = '/home/lin/Desktop/data/lits/tumor_seg'

livers = os.listdir(liver_dir)

def comb(fnames):
	print(len(fnames))
	for fname in fnames:
		print(fname)
		liverf = nib.load(os.path.join(liver_dir, fname))
		tumorf = nib.load(os.path.join(tumor_dir, fname))

		liver = liverf.get_fdata()
		tumor = tumorf.get_fdata()
		print(liver.shape, tumor.shape)

		liver[tumor == 1] = 2

		newf = nib.Nifti1Image(liver, np.eye(4))
		nib.save(newf, "/home/lin/Desktop/data/lits/combo" + fname)

# threads = [threading.Thread(target=comb, args=(livers[i * len(livers)//4: (i+1)*len(livers)//4], ) ) for i in range(4)]
# threads.append(threading.Thread(target=comb, args=(livers[4 * len(livers)//4:], ) ) )
#
# for thread in threads:
# 	thread.start()

comb(livers)
