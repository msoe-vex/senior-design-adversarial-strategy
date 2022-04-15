#!/bin/bash

#SBATCH --partition=teaching
#SBATCH --cpus-per-task=2

module purge
eval "$(conda shell.bash hook)"
conda activate vex_adversarial

python src/training.py
