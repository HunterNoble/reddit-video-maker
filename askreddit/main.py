from types import NoneType
from utils.redditScrape import scrapeComments
from utils.audioGenerator import soundifyAuthor, soundifyComment
# from utils.audioEleven import soundifyAuthor, soundifyComment
# from utils.audioGTTS import soundifyAuthor, soundifyComment
from utils.captionCreate import commentImage, titleImage, commentBlankImage
from utils.videoCreate import createVideo
import shutil
import os
import time
import concurrent.futures

# Gets posts and top x comments from selected subreddit
### subreddit, number of posts, timeframe
# for i in range(num_of_posts):
def process_video(i):
    #for file in os.listdir("temp"):
    #    os.remove("temp/"+file)
    
    postnum = i + 1
    # scrape best post i to create movie
    post = scrapeComments("askreddit", postnum, "day")
    # DEBUG
    # print(post[0].author)

    # get post author
    asker = str(post[0].author)

    skip = False

    # skip if video already exists for asker - probably a cleaner way to do this
    for files in os.listdir('../exports'):
        if asker + '.mp4' in files:
            print ('File already exists for thread.\n')
            skip = True
    if skip:
        print ('Skipping post by: ' + asker)
        # continue
        return

    # delete post directory if already exists
    if os.path.isdir(asker):
        shutil.rmtree(asker)
    
    # get subreddit of post
    subreddit = str(post[0].subreddit)

    # create directory to store files
    os.makedirs(asker)

    if len(post) > 1:
        post.insert(1, {'author':'', 'body':'Don\'t forget to follow!'})
        # post[1].author = asker
    if len(post) > 7:
        post.insert (5, {'author':'', 'body':'If you hold the comment button, you will see your 4 most used emoji'})
    if len(post) > 12:
        post.insert (9, {'author':'', 'body':'The third name you see when you click Share then More secrelty has a crush on you'})
        
    # if len(post) > 3:
    #     post.insert(3, asker, 'If you hold the comment button, you will see your 4 most used emoji')
    #     post[1].author = asker
    #     commentBlankImage(post[3], 3, asker)
    
    for j in range(len(post)):
        try:
            if post[j].author is None:
                # set post author to [deleted] if no post author found
                author = "[deleted]"
            else:
                try:
                    author = post[j].author.name
                except:
                    author = "[deleted]"
        except AttributeError:
            pass

        if j == 0:
            # if title post, print title caption with post name and info
            # print(post[j].title)
            titleImage(post[j].title, author, "r/"+subreddit)
            soundifyAuthor(post[j].title, asker)
        else:
            # if not title post, create comment caption
            try:
                text = post[j].body
            except AttributeError:
                text = post[j]['body']

            # DEBUG
            # print(text)
            sections = []

            # control size of caption to fit it on the screen vertically
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
                if sections[section] != '':
                    try:
                        if post[j]['author'] == '':
                            commentBlankImage(sections[section], j, asker)
                            soundifyComment(sections[section], j, section, asker)
                    except TypeError:
                        commentImage(author, sections[section], j, section, asker)
                        soundifyComment(sections[section], j, section, asker)

    # # create audio for title caption
    # soundifyAuthor(post[0].title, asker)

    if post[0].author is None:
        author = "[deleted]"
    else:
        author = post[0].author.name

    createVideo(author)

if __name__ == '__main__':
    t1 = time.perf_counter()

    # input of how many posts to scrape
    num_of_posts = input('How many videos would you like to create?\n')
    while not num_of_posts.isnumeric():
        num_of_posts = input('That was not a number. How many videos would you like to create?\n')
    num_of_posts = int(num_of_posts)

    # multiprocessing to speed up video creation
    with concurrent.futures.ProcessPoolExecutor() as executor:
    # with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(num_of_posts):
            executor.submit(process_video, i)

    t2 = time.perf_counter()

    print(f'Finished in {t2-t1} seconds')

# TikTok tags
# #fyp #foryoupage #askreddit #reddit #askredditstories #redditreadings #reddittts