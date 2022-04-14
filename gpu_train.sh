#!/bin/bash

#SBATCH --partition=teaching
#SBATCH --gres=gpu:t4:1
#SBATCH --cpus-per-gpu=2

module purge
eval "$(conda shell.bash hook)"
conda activate vex_adversarial

python src/training.py
