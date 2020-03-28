vol_path='/home/lin/Desktop/data/ann/vol/'
lab_path='/home/lin/Desktop/data/ann/lab/'

for name in `ls $lab_path`
do
  echo $name
#  itksnap -g $vol_path$name -s $lab_path$name &
  itksnap -g $vol_path$name -s $flood_path$name
done
