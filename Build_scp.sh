#!/bin/bash

sample_sheet=$1
destination=$2

# 1. Convert and creaate scp for SampleSheet
echo "Check_SampleSheet.py ${sample_sheet} > ${sample_sheet%.*}.tmp"
echo "scp ${sample_sheet%.*}.tmp ${destination}/${sample_sheet}"

to_print=""
while read line; do 
	new_name=$(echo ${line} | cut -f1 -d',')
	old_name=$(echo ${line} | cut -f9 -d',')
	echo "scp ${old_name} ${destination}/data/${new_name}.single.fastq.gz"
done < <(Check_SampleSheet.py ${sample_sheet} | tail -n+2)
