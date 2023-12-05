#!/bin/bash

# This script formats smth-smth data.
SMTH_SMTH_DIR="./something-something-v2"
cd $SMTH_SMTH_DIR

# 1. Download train.csv and val.csv split given by openvclip
# Edit: We actually do not need these files, commenting just in case one wants to download to have a comparison of the result we are achieving
# mkdir -p labels
# curl https://dl.fbaipublicfiles.com/pyslowfast/dataset/ssv2/frame_lists/train.csv -o ./labels/train.csv
# curl https://dl.fbaipublicfiles.com/pyslowfast/dataset/ssv2/frame_lists/val.csv -o ./labels/val.csv

# Uses ffmpeg to split all the videos in jpg images with the folder structure specified in train.csv
VIDEO_DIR="20bn-something-something-v2"
cd $VIDEO_DIR

# Be aware that this is painfully slow
for VIDEO in $(ls)
do
    VIDEO_NUM=$( echo ${VIDEO} | cut -d '.' -f1) 
    mkdir -p ${VIDEO_NUM} 
    ffmpeg -i ${VIDEO} -r 30 -q:v 1 ${VIDEO_NUM}/${VIDEO_NUM}_%03d.jpg 
    mv ${VIDEO} ${VIDEO_NUM}
done
