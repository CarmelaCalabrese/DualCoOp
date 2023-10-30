import cv2
import numpy
import yt_dlp as youtube_dl
import os
import re
import time

def video_to_frames_url_auto(second, url=None, folder='/home/cc/projects/'):
    """Function to extract frames from input video url or file and save them as separate frames 
    in an output directory. Output directory will be named starting from video_1. If a new file is downloaded,
    a video_2 folder will be created and so on.
    Dependencies: 
        OpenCV
        youtube-dl (sudo pip install --upgrade youtube_dl)
    
    Args:
        url: Youtube video URL.
        folder: Directory to download and save each frames.
        
    Returns:
        None
        
    Work to be done:
    1. Handle exceptions
    """
    
    # Log start time
    time_start = time.time()
    
    os.mkdir("video_1")
    # Create a folder according to the files that are already present.   
    #os.mkdir("video_" + str(newfile))
    
    file_loc = folder + "video_1" + "/video_1.mp4"
    # Download from local video file
    if (url):
        print("Downloading Youtube Video")
        os.system("youtube-dl -o " + file_loc + " -f mp4 " + url)
        cap = cv2.VideoCapture(file_loc)
    else:
        print("This is where I should raise an error. --EXCEPTION HANDLING--")

###
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame = int(second) *fps
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
    # success,image = cap.read()
    # count = 0
    #while success and count==0:
    # print('sono qui')
    # cv2.imwrite("frame%d.jpg" % frame, image)     # save frame as JPEG file      
    # success,image = cap.read()
    # print('Done: ', success)

###
    # video_length = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)) - 1
    # print "Number of frames: ", video_length
    count = 0
    print ("Converting video..\n")
    while cap.isOpened():
        ret,frame = cap.read()
        if(count==frame):
            cv2.imwrite(folder + "video_" + str(newfile) + "/%d.jpg" % (count+1), frame)
        count = count + 1
        if (count > (video_length-1)):
            time_end = time.time()
            cap.release()
            #print "Done extracting frames.\n%d frames extracted" %count
            print("Done extracting frames.\n%d frames extracted" %count)
            #print "It took %d seconds for conversion." %(time_end-time_start)
            break

video_to_frames_url_auto(902,'https://www.youtube.com/watch?v=-5KQ66BBWC4&t=904s', './')