from moviepy.editor import *
from moviepy.video import *
from moviepy.video.fx.all import crop
import moviepy.editor as mpe
import os
import random
import time
import shutil
from datetime import datetime
import re


def createVideo(username):
    audioClip = []
    imageClip = []
    length = -0.5
    res_x = 720
    res_y = 1080

    startTimes = [0]

    if os.path.exists(username+"/constructed.mp4"):
        os.remove(username+"/constructed.mp4")
    
    def atoi(text):
        return int(text) if text.isdigit() else text

    def natural_keys(text):
        return [ atoi(c) for c in re.split(r'(\d+)', text) ]

    for files in sorted(os.listdir(username+""), key=natural_keys):
        if ".mp3" in files:
            audio = AudioFileClip(username+"/"+files)
            audioClip.append(audio.set_start(length+0.5))
            length += audio.duration + 0.5
            startTimes.append(length)
            
    i = 0
    for files in sorted(os.listdir(username+""), key=natural_keys):

        if ".png" in files:
            clip = ImageClip(username+"/"+files,duration=audioClip[i].duration).set_start(startTimes[i])
            
            (w,h) = clip.size
            clip = clip.resize((w*1.25,h*1.25))
            (w,h) = clip.size
            clip = clip.set_position((res_x/2-w/2,res_y/2-h/2))
            clip = clip.set_opacity(1)
            imageClip.append(clip)
            i += 1
            clip.close()
    i = 0

    #videoImages = CompositeVideoClip(imageClip)
    videoAudio = CompositeAudioClip(audioClip)

    # backgroundClip = ColorClip((720,1280), (0,0,255), duration=videoAudio.duration)
    bg_file = os.listdir("../bg_vids")[random.randrange(0,len(os.listdir("../bg_vids")))]
    backgroundClip = VideoFileClip("../bg_vids/"+bg_file)

    # set background clip to short form media size
    backgroundClip = crop(backgroundClip, x_center=backgroundClip.w/2, y_center=backgroundClip.h/2, width=res_x, height=res_y)

    # determine latest point in background clip that it can start at
    # randomly select a point in background clip between start and latest point
    # background clip = section of video between the selected start point and end point determined by video length
    if videoAudio.duration < 61:
        videoStart = int(backgroundClip.duration - 61)
        videoStart = random.randrange(0,videoStart)
        backgroundClip = backgroundClip.subclip(videoStart, videoStart + 61)
    else:
        videoStart = int(backgroundClip.duration-videoAudio.duration)
        videoStart = random.randrange(0,videoStart)
        backgroundClip = backgroundClip.subclip(videoStart, videoStart + videoAudio.duration + 1)

    print(bg_file)
    #(w, h) = videoImages.size

    #videoImages.crop(width=720,height=1280, x_center=w/2, y_center=h/2)
    
    videoClip = backgroundClip
    videoClip = CompositeVideoClip([videoClip] + imageClip)


    audio_background = mpe.AudioFileClip("../music/"+os.listdir("../music")[random.randrange(0,len(os.listdir("../music")))])

    # create music to last video duration
    while audio_background.duration < videoClip.duration:
        # audio_background = concatenate_audioclips([audio_background, mpe.AudioFileClip("../music/"+os.listdir("../music")[random.randrange(0,len(os.listdir("../music")))])])
        audio_background = concatenate_audioclips([audio_background, audio_background])
    
    # audio_background.fx(afx.volumex, 0.9)

    # final audio that will be put over video
    final_audio = mpe.CompositeAudioClip([videoAudio, audio_background.fx(afx.volumex, 0.25)]).set_duration(backgroundClip.duration)
    videoClip.audio = final_audio

    # adjust videoClip speed
    # videoClip = videoClip.fx(vfx.speedx, 1.1)

    # create mp4 file
    videoClip.write_videofile("../exports/"+datetime.now().strftime("%Y-%m-%d %H-%M-%S - ")+username+".mp4", fps=30)

    backgroundClip.close()
    videoClip.close()
    videoAudio.close()
    audio_background.close()
    final_audio.close()

    time.sleep(3)

    # remove temp directory
    shutil.rmtree(username+"")

    # time.sleep(5)

    

    '''while len(os.listdir(username+"")) > 0:
        for files in os.listdir(username+""):
            if ".mp3" in files or ".png" in files: 
                try:
                    os.remove(username+"/"+files)
                except:
                    continue'''

if __name__ == "__main__":
    createVideo("post")
