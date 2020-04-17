vol_path='/home/lin/Desktop/data/aorta/volume/'
lab_path='/home/lin/Desktop/data/aorta/lab_inf/'

for name in `ls $lab_path`
do
  echo $name
 	itksnap -g $vol_path$name -s $lab_path$name 
  # itksnap -g $vol_path$name -s $flood_path$name
done
