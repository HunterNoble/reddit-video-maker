import elevenlabs
from .info import eleven_labs_api_key

elevenlabs.set_api_key(eleven_labs_api_key)

voice = elevenlabs.Voice(
    voice_id = '21m00Tcm4TlvDq8ikWAM',
)
#voice = 'Natasha'

def soundifyAuthor(title, asker):
    audio = elevenlabs.generate(
        text = title,
        voice = voice,
    )
    elevenlabs.save(audio, asker+'/temp'+'0'+'.mp3')

def soundifyComment(comment, index, sectionid, asker):
    audio = elevenlabs.generate(
        text = comment,
        voice = voice,
    )
    elevenlabs.save(audio, asker+'/temp'+str(index)+'_'+str(sectionid)+'.mp3')