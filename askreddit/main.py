from types import NoneType
from utils.redditScrape import scrapeComments
from utils.audioGenerator import soundifyAuthor, soundifyComment, soundifyFollow, soundifyMakeComment
# from utils.audioEleven import soundifyAuthor, soundifyComment
from utils.captionCreate import commentImage, titleImage, commentBlankImage
from utils.videoCreate import createVideo
import shutil
import os
import time

# Gets posts and top x comments from selected subreddit
### subreddit, number of posts, timeframe


for i in range(5):
    #for file in os.listdir("temp"):
    #    os.remove("temp/"+file)
    
    postnum = i + 1
    # scrape best post i to create movie
    post = scrapeComments("askreddit", postnum, "day")
    # debug line
    print(post[0].author)

    # get post author
    asker = str(post[0].author)

    if os.path.isdir(asker):
        shutil.rmtree(asker)
    
    # get subreddit of post
    subreddit = str(post[0].subreddit)

    # create directory to store files
    os.makedirs(asker)

    # if len(post) > 1:
    #     post.insert(1, 'Don\'t forget to follow!')
    #     post[1].author = asker
    #     commentBlankImage(post[1], 1, asker)
    # if len(post) > 3:
    #     post.insert(3, 'If you hold the comment button, you will see your 4 most used emoji')
    #     post[1].author = asker
    #     commentBlankImage(post[3], 3, asker)

    for j in range(len(post)):
        

        if post[j].author is None:
            # set post author to [deleted] if no post author found
            author = "[deleted]"
        else:
            try:
                author = post[j].author.name
            except:
                author = "[deleted]"
        if j == 0:
            # if start of post, print title caption with post name and info
            print(post[j].title)
            titleImage(post[j].title, author, "r/"+subreddit)
        else:
            if j == 2:
                # makeshift way to add a call to action until a better method can be added - replaces comment content
                text = 'Don\'t forget to follow!'
            elif j == 5:
                # makeshift way to add a call to action until a better method can be added - replaces comment content
                text = 'Holding the comment button shows your 4 most used emojis'
            else:
                # sets text to comment content
                text = post[j].body
            print(text)
            sections = []

            # control size of caption to keep it on the screen
            if len(text) > 500:
                length = 0
                nextSpace = 0
                for k in range(len(text)):
                    if k % 300 == 0:
                        if text[k] == ".":
                            nextSpace = k + 1
                            sections.append(text[length:nextSpace])
                            length = nextSpace
                        else:
                            for l in range(len(text[:k])):
                                if text[l] == ".":
                                    nextSpace = l + 1
                                    
                            sections.append(text[length:nextSpace])
                            length = nextSpace

                sections.append(text[length:len(text)])
                sections = sections[1:]
            else:
                sections.append(text)
            
            # create captions and audio for thread comments
            for section in range(len(sections)):
                commentImage(author, sections[section], j, section, asker)
                soundifyComment(sections[section], j, section, asker)

    # create audio for title caption
    soundifyAuthor(post[0].title, asker)

    if post[0].author is None:
        author = "[deleted]"
    else:
        author = post[0].author.name
    createVideo(author)