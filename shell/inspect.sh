vol_path='/home/lin/Desktop/vol_nii/'
flood_path='/home/lin/Desktop/data/aorta/flood/'
lab_path='/home/lin/Desktop/lab_ref/'

for name in `ls $vol_path`
do
  echo $name
#  itksnap -g $vol_path$name -s $lab_path$name &
  itksnap -g $vol_path$name -s $flood_path$name
done
