from moviepy.editor import *
from moviepy.video import *
from moviepy.video.fx.all import crop
import moviepy.editor as mpe
import os
import random
import time
import shutil


def createVideo(username):
    audioClip = []
    imageClip = []
    length = -0.5
    res_x = 720
    res_y = 1080

    startTimes = [0]

    if os.path.exists(username+"/constructed.mp4"):
        os.remove(username+"/constructed.mp4")
    

    for files in os.listdir(username+""):
        if ".mp3" in files: 
            audioClip.append(AudioFileClip(username+"/"+files).set_start(length+0.5))
            length += AudioFileClip(username+"/"+files).duration + 0.5
            startTimes.append(length)
            
    i = 0
    for files in os.listdir(username+""):

        if ".png" in files:
            clip = ImageClip(username+"/"+files,duration=audioClip[i].duration).set_start(startTimes[i])
            

            (w,h) = clip.size
            # clip = clip.resize(newsize=(w*1.5,h*1.5))
            clip = clip.resize((w*1.25,h*1.25))
            # (w,h) = (w*1.5,h*1.5)
            (w,h) = clip.size
            # clip = clip.set_position((540-w/2,960-h/2))
            clip = clip.set_position((res_x/2-w/2,res_y/2-h/2))
            clip = clip.set_opacity(1)
            imageClip.append(clip)
            i += 1
    i = 0

    #videoImages = CompositeVideoClip(imageClip)
    videoAudio = CompositeAudioClip(audioClip)

    # backgroundClip = ColorClip((720,1280), (0,0,255), duration=videoAudio.duration)
    bg_file = os.listdir("../bg_vids")[random.randrange(0,len(os.listdir("../bg_vids")))]
    backgroundClip = VideoFileClip("../bg_vids/"+bg_file)
    backgroundClip = crop(backgroundClip, x_center=backgroundClip.w/2, y_center=backgroundClip.h/2, width=res_x, height=res_y)
    videoStart = int(backgroundClip.duration-videoAudio.duration)
    videoStart = random.randrange(0,videoStart)
    backgroundClip = backgroundClip.subclip(videoStart, videoStart + videoAudio.duration + .75)
    print(bg_file)
    #(w, h) = videoImages.size

    #videoImages.crop(width=720,height=1280, x_center=w/2, y_center=h/2)
    
    videoClip = backgroundClip
    videoClip = CompositeVideoClip([videoClip] + imageClip)
    audio_background = mpe.AudioFileClip("../music/"+os.listdir("../music")[random.randrange(0,len(os.listdir("../music")))])

    # create music to last video duration
    while audio_background.duration < videoClip.duration:
        audio_background = concatenate_audioclips([audio_background, mpe.AudioFileClip("../music/"+os.listdir("../music")[random.randrange(0,len(os.listdir("../music")))])])
    
    # audio_background.fx(afx.volumex, 0.9)

    # final audio that will be put over video
    final_audio = mpe.CompositeAudioClip([videoAudio, audio_background.fx(afx.volumex, 0.1)]).set_duration(backgroundClip.duration)
    videoClip.audio = final_audio

    # create mp4 file
    videoClip.write_videofile("../exports/"+username+".mp4", fps=30)

    # remove temp files
    shutil.rmtree(username+"")

    time.sleep(5)

    

    '''while len(os.listdir(username+"")) > 0:
        for files in os.listdir(username+""):
            if ".mp3" in files or ".png" in files: 
                try:
                    os.remove(username+"/"+files)
                except:
                    continue'''

if __name__ == "__main__":
    createVideo("post")
