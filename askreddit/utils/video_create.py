from moviepy.editor import *
from moviepy.video import *
from moviepy.video.fx.all import crop
from datetime import datetime
import moviepy.editor as mpe
import os, random, time, shutil, re

def create_video(username):
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

    for files in sorted(os.listdir(str(username)), key=natural_keys):
        if ".mp3" in files:
            audio = AudioFileClip(username+"/"+files)
            audioClip.append(audio.set_start(length+0.5))
            length += audio.duration + 0.5
            startTimes.append(length)
            
    i = 0
    for files in sorted(os.listdir(str(username)), key=natural_keys):

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

    #videoImages = Compositevideo_clip(imageClip)
    video_audio = CompositeAudioClip(audioClip)

    # background_clip = ColorClip((720,1280), (0,0,255), duration=video_audio.duration)
    bg_file = os.listdir("../bg_vids")[random.randrange(0,len(os.listdir("../bg_vids")))]
    background_clip = VideoFileClip("../bg_vids/"+bg_file)

    # set background clip to short form media size
    background_clip = crop(background_clip, x_center=background_clip.w/2, y_center=background_clip.h/2, width=res_x, height=res_y)

    # determine latest point in background clip that it can start at
    # randomly select a point in background clip between start and latest point
    # background clip = section of video between the selected start point and end point determined by video length
    if video_audio.duration < 61:
        video_start = int(background_clip.duration - 61)
        video_start = random.randrange(0,video_start)
        background_clip = background_clip.subclip(video_start, video_start + 61)
    else:
        video_start = int(background_clip.duration-video_audio.duration)
        video_start = random.randrange(0,video_start)
        background_clip = background_clip.subclip(video_start, video_start + video_audio.duration + 1)

    print(bg_file)
    #(w, h) = videoImages.size

    #videoImages.crop(width=720,height=1280, x_center=w/2, y_center=h/2)
    
    video_clip = background_clip
    video_clip = CompositeVideoClip([video_clip] + imageClip)


    audio_background = mpe.AudioFileClip("../music/"+os.listdir("../music")[random.randrange(0,len(os.listdir("../music")))])

    # create music to last video duration
    while audio_background.duration < video_clip.duration:
        # audio_background = concatenate_audioclips([audio_background, mpe.AudioFileClip("../music/"+os.listdir("../music")[random.randrange(0,len(os.listdir("../music")))])])
        audio_background = concatenate_audioclips([audio_background, audio_background])

    # final audio that will be put over video
    final_audio = mpe.CompositeAudioClip([video_audio, audio_background.fx(afx.volumex, 0.25)]).set_duration(background_clip.duration)
    video_clip.audio = final_audio

    # adjust video_clip speed
    # video_clip = video_clip.fx(vfx.speedx, 1.1)

    # create mp4 file
    video_clip.write_videofile("../exports/"+datetime.now().strftime("%Y-%m-%d %H-%M-%S - ")+username+".mp4", fps=60)

    background_clip.close()
    video_clip.close()
    video_audio.close()
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
    create_video("post")
