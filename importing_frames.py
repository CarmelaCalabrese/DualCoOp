import cv2
import numpy
import yt_dlp as youtube_dl


second = '904'
url_id = f'-5KQ66BBWC4&t={second}s'
saved_url=f'https://www.youtube.com/watch?v={url_id}'

url=saved_url #The Youtube URL
ydl_opts={}
ydl=youtube_dl.YoutubeDL(ydl_opts)
info_dict=ydl.extract_info(url, download=False)

formats = info_dict.get('formats',None)
print("Obtaining frames")

for f in formats:
    if f.get('format_note',None) == '144p':
        url = f.get('url',None)
        cap = cv2.VideoCapture(url)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        print('fps')
        print(fps)
        frame = int(second)*fps
        print('frame')
        print(frame)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        success,image = cap.read()
        count = 0
        while success and count==0:
            print('sono qui')
            cv2.imwrite("frame%d.jpg" % frame, image)     # save frame as JPEG file      
            count += 1
            print('Done: ', success)


