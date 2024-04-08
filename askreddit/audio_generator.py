import pyttsx3, random

engine = pyttsx3.init()

voices = engine.getProperty('voices')
#engine.setProperty('voice', voices[0].id)


def soundify_author(title, asker):

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    engine.save_to_file(title, asker+"/temp"+"0"+".mp3")
    engine.runAndWait()


def soundify_comment(comment, index, sectionid, asker):
    
    '''
    swears = ["fuck", "shit"]

    comment = comment.split()

    for word in comment:
        if word in swears:
            print("yikes")

    ' '.join(comment)
    '''
    
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    engine.save_to_file(comment, asker+"/temp"+str(index)+"_"+str(sectionid)+".mp3")
    engine.runAndWait()

'''
for voice in voices:
    print(voice, voice.id)
    engine.setProperty('voice', voice.id)
    engine.say("Hello World!")
    engine.runAndWait()
    engine.stop()
'''