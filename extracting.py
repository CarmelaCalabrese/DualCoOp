from pytube import YouTube
import cv2
import pandas as pd
import json
import ast
import numpy as np

def frame_extraction (url_id, second, name):

    try:
        # Replace 'VIDEO_URL' with the URL of the YouTube video
        #url_id = f'-5KQ66BBWC4'
        video_url=f'https://www.youtube.com/watch?v={url_id}'

        # Create a YouTube object
        yt = YouTube(video_url)

        # Get the video stream without downloading the entire video
        stream = yt.streams.get_highest_resolution()

        # Use OpenCV to extract a frame at a specific time (in seconds)
        # Replace 'time_in_seconds' with the desired time
        time_in_seconds = second
        cap = cv2.VideoCapture(stream.url)
        cap.set(cv2.CAP_PROP_POS_MSEC, time_in_seconds * 1000)
        ret, frame = cap.read()

        if ret:
            # Save the extracted frame as an image
            cv2.imwrite(f'./frames_value2/{name}.jpg', frame)
        else:
            print("Frame extraction failed.")

        # Release the video capture object
        cap.release()

    except Exception as e:
        print(f"An error occurred for {url_id}-{second}: {e}")

our_dataset = pd.read_csv('./output_values2.csv')

print('Estraggo')
annotations= []
for index, row in our_dataset.iterrows():
    if index<1280:
        continue
    print('index')
    print(index)
    frame_extraction(row['url_id'], row['Second'], f'url_{index}')
    ann_vec = [0]*80
    actions_lab = row['Actions_id']
    actions_lab = [int(x) for x in actions_lab.replace('[','').replace(']','').split()]
    print('Actions idx:')
    for idx, val in enumerate(actions_lab):
        print(val)
        ann_vec[int(val)-1] = 1
    #print(ann_vec)
    annotations.append(ann_vec)

print(annotations)
np.save('./frames_value1/annotations_values2.npy', annotations)
print('finito')