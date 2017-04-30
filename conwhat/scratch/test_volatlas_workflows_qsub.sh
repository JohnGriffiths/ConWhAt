#!/bin/bash
#$ -S /bin/bash
#$ -q abaqus.q
#$ -l qname=abaqus.q
#$ -V
#$ -cwd
#$ -M j.davidgriffiths@gmail.com
#$ -m be

#use freesurfer
use fsl

export PATH="/home/hpc3230/Software/anaconda2/bin:$PATH"

source activate tvb # dipy_release

python /home/hpc3230/Code/libraries_of_mine/github/ConWhAt/conwhat/scratch/test_volatlas_workflows.py




