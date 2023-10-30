import cv2
import numpy
import yt_dlp as youtube_dl

# import shlex
# command = shlex.split('ffmpeg -ss 902 -i $(youtube-dl -f 22 --get-url https://www.youtube.com/watch?v=-5KQ66BBWC4) -vframes 1 -q:v 2 ./prova.jpeg')

# print('Fatto')

second = '904'
url_id = f'-5KQ66BBWC4&t={second}s'
saved_url=f'https://www.youtube.com/watch?v={url_id}'

url=saved_url #The Youtube URL
ydl_opts={}
ydl=youtube_dl.YoutubeDL(ydl_opts)
info_dict=ydl.extract_info(url, download=False)

formats = info_dict.get('formats',None)
print("Obtaining frames")
# for f in formats:
#     if f.get('format_note',None) == '144p':
#         url = f.get('url',None)
#         cap = cv2.VideoCapture(url)
#         x=0
#         count=0
#         while x<10:
#             ret, frame = cap.read()
#             if not ret:
#                 break
#             filename =r"PATH\shot"+str(x)+".png"
#             x+=1
#             cv2.imwrite(filename.format(count), frame)
#             count+=300 #Skip 300 frames i.e. 10 seconds for 30 fps
#             cap.set(1,count)
#             if cv2.waitKey(30)&0xFF == ord('q'):
#                 break
#         cap.release()


for f in formats:
    if f.get('format_note',None) == '144p':
        url = f.get('url',None)
        cap = cv2.VideoCapture(url)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame = int(second*fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        success,image = cap.read()
        count = 0
        #while success and count==0:
        print('sono qui')
        cv2.imwrite("frame%d.jpg" % frame, image)     # save frame as JPEG file      
        success,image = cap.read()
        print('Done: ', success)
