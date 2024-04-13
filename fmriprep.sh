#!/bin/bash
#Template provided by Daniel Levitas of Indiana University
#Edits by Andrew Jahn, University of Michigan, 07.22.2020

#User inputs:
bids_root_dir='media/agniswar/New Volume/test for preprocessing/scaffold/'
subj=02
nthreads=4
container=docker #docker or singularity



fmriprep-docker $bids_root_dir $bids_root_dir/derivatives \
    participant --participant-label $subj \
    --skip-bids-validation \
    --md-only-boilerplate \
    --fs-license-file '/media/agniswar/New Volume/test for preprocessing/scaffold/license.txt' \
    --fs-no-reconall \
    --output-spaces MNI152NLin2009cAsym:res-2 \
    --low-mem \
    --stop-on-first-crash \