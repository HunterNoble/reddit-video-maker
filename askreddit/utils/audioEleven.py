import elevenlabs
import os
from dotenv import load_dotenv

load_dotenv()

# set API key for eleven labs
elevenlabs.set_api_key(os.getenv('ELEVENLABS_API_KEY'))

# set voice - 'Rachel'
voice = elevenlabs.Voice(
    voice_id = '21m00Tcm4TlvDq8ikWAM',
)

# generate speech for self post
def soundifyAuthor(title, asker):
    audio = elevenlabs.generate(
        text = title,
        voice = voice,
    )
    elevenlabs.save(audio, asker+'/temp'+'0'+'.mp3')

# generate speech for comments
def soundifyComment(comment, index, sectionid, asker):
    audio = elevenlabs.generate(
        text = comment,
        voice = voice,
    )
    elevenlabs.save(audio, asker+'/temp'+str(index)+'_'+str(sectionid)+'.mp3')