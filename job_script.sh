#!/bin/bash
#SBATCH -A ayush.singhania
# SBATCH --reservation ndq
#SBATCH --gres=gpu:1
#SBATCH -c 10
#SBATCH --mail-type=ALL
#SBATCH --mail-user=ayush.singhania@students.iiit.ac.in
#SBATCH --time=4-00:00:00
#SBATCH --output=out.txt
#SBATCH --mem-per-cpu=3072


module add cuda/9.0
module load cudnn/7-cuda-9.0
module load matlab
#source activate torch
cd /scratch/
if [ -d "pratyush1999_SRFB" ]; then
        rm -rf pratyush1999_SRFB
fi

mkdir -p pratyush1999_SRFB
cp -r /home/pratyush1999/SRFBN_CVPR19/ /scratch/pratyush1999_SRFB/

cd /scratch/pratyush1999_SRFB/SRFBN_CVPR19
source venv/bin/activate
unzip  DIV2K_train_HR.zip
unzip DIV2K_valid_HR.zip
matlab -nodisplay -nosplash -nodesktop -r "run('./scripts/Prepare_TrainData_HR_LR.m');exit;"
matlab -nodisplay -nosplash -nodesktop -r "run('./results/Prepare_TestData_HR_LR.m');exit;"
python train.py -opt options/train/train_SRFBN_example.json
