#!/bin/bash

#echo "Czekam 3h.."
#sleep 3h
#skrypt uruchamia symulacje w katalogach symulacji
echo "Uruchamiam symulacje..."

#cp -p ./srednia/template/* ./

#start_path=$PWD

#sim_dir=$start_path/data/$1

#script_path=$start_path/scripts
#template_path=$start_path/template


#rm -r data
#mkdir data


cd data

for kat in ./S*; do
    cd $kat
	id_job=$(sbatch run_sim)
	echo $id_job >> jobs_id

#	ind=`cat jobid`
#	scancel $ind
    cd ..
done

cd ..
