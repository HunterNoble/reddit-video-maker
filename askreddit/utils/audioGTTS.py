from gtts import gTTS

def soundifyAuthor(title, asker):
    tts = gTTS(title)
    tts.save(asker+'/temp'+'0'+'.mp3')

def soundifyComment(comment, index, sectionid, asker):
    tts = gTTS(comment)
    tts.save(asker+'/temp'+str(index)+'_'+str(sectionid)+'.mp3')