vol_path='/home/aistudio/data/inference'
lab_path='/home/aistudio/data/inf_lab'

for name in `ls $vol_path`
do
  echo $name
  # itksnap -g $vol_path/$name -s $lab_path$name 
  itksnap -g $vol_path/$name -s $lab_path/test-segmentation${name:11}
  # itksnap -g $vol_path$name -s $flood_path$name
done
