vol_path='/home/lin/Desktop/vol_nii/'
flood_path='/home/lin/Desktop/data/aorta/flood/'
zip_path='/home/lin/Desktop/data/aorta/zip/'

touch ${zip_path}dumb
rm ${zip_path}* -rf

mkdir ${zip_path}volume
mkdir ${zip_path}label

for name in `ls $vol_path `
do
  cp $vol_path$name ${zip_path}volume/
  cp $flood_path$name ${zip_path}label/
done

tar -cvf /home/lin/Desktop/studio.tar ${zip_path}volume ${zip_path}label
