#!/bin/bash

# One script to run them all

if ! ls cookie.txt 2>/dev/null
then
    echo "You need a cookie.txt file with your authentication data!"
    return
fi

cat cookie.txt | ./download_smth_smth.sh -p 
./ssv2_frame_split.sh
python3 ssv2_preprocessing.py