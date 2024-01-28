#!/bin/bash
#SBATCH --job-name=Qrcode
#SBATCH --array=1-10
#SBATCH --time=00:15:30 # days-hh-mm-ss
#SBATCH --mem-per-cpu=512 #megabytes

ml Python
ml matplotlib

echo "Task_ID : $SLURM_ARRAY_TASK_ID"
python Qrcode.py $SLURM_ARRAY_TASK_ID
