#!/bin/bash


#Run this file
#./test.sh inputfolder outputfolder
now=$(date)
echo "$now"

#omega=('0.01' '0.02' '0.03' '0.04' '0.05' '0.06' '0.07' '0.08' '0.09' '0.1')
omega=('0.1' '0.01' '0.2' '0.02' '0.03' '0.03' '0.4' '0.04' '0.5' '0.05' '0.6' '0.06' '0.7' '0.07' '0.8' '0.08' '0.9' '0.09' '0.005' '0.006')
array=('0.01' '0.01' '0.01' '0.01' '0.01' '0.01' '0.01' '0.01' '0.01' '0.01')
output=$2
for dir in $1/*
do
    for file in $dir/*processed*
    do
        data=$file
        rank=${file/processed/rank}
        name=${file/processed/0name}
        
        for((x=1; x <= 5 ; x++))
        do 
            array=('0.01' '0.01' '0.01' '0.01' '0.01' '0.01' '0.01' '0.01' '0.01' '0.01')
            for i in "${omega[@]}"
	        do
  		        for j in "${omega[@]}"
    	        do {
    			 array[2*$x - 1]=$i
    			 array[2*$x]=$j

			     params=$(printf ",%s" "${array[@]}")
			     params=${params:1}

			     echo $params
        	     
                 now=$(date +"%T")
        		 echo "Current time : $now", $f
                 echo $data $rank $name $output
        		 #echo "Rscript main.R ${data} ${rank} ${name} ${output}${x}${i}${j} $params"
                 Rscript main.R ${data}'0.txt' ${data}'rank0temp.txt' ${data}'0name.txt' ${output}${x}${i}${j} $params 
                } ||
                {
                   echo "Error $i $j"
                }
                #break
                now=$(date +"%T")
                echo "Current time : $now"
                done       
      	    done
		    #break
        done
	    #break
    done
done

now=$(date)
echo "$now"

