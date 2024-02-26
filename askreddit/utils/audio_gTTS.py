from gtts import gTTS

def soundify_author(title, asker):
    tts = gTTS(title)
    tts.save(asker+'/temp'+'0'+'.mp3')

def soundify_comment(comment, index, sectionid, asker):
    tts = gTTS(comment)
    tts.save(asker+'/temp'+str(index)+'_'+str(sectionid)+'.mp3')