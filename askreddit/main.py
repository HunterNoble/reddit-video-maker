from types import NoneType
from utils.reddit_scrape import scrape_comments
from utils.audio_generator import soundify_author, soundify_comment
# from utils.audio_eleven import soundify_author, soundify_comment
# from utils.audio_gTTS import soundify_author, soundify_comment
from utils.caption_create import comment_image, title_image, comment_blank_image
from utils.video_create import create_video
import shutil, os, time, concurrent.futures

# Gets posts and top x comments from selected subreddit
### subreddit, number of posts, timeframe
# for i in range(num_of_posts):
def process_video(i):
    postnum = i + 1
    # scrape best post i to create movie
    post = scrape_comments("askreddit", postnum, "day")
    # get post author
    asker = str(post[0].author)

    print(f'\nScraped post {postnum}.')

    # skip if video already exists for asker - probably a cleaner way to do this
    for files in os.listdir('../exports'):
        if asker + '.mp4' in files:
            print (f'File already exists for {asker}.\nThis was post {postnum}.\n')
            return None
    print(f'Creating post for {asker}. This is post {postnum}.')

    # delete post directory if already exists
    if os.path.isdir(asker):
        shutil.rmtree(asker)
    
    # get subreddit of post
    subreddit = str(post[0].subreddit)

    # create directory to store files
    os.makedirs(asker)

    if len(post) > 1:
        post.insert(1, {'author':'', 'body':'Share your thoughts in the comments'})
    if len(post) > 2:
        post.insert (4, {'author':'', 'body':'Don\'t forget to follow!'})
    if len(post) > 12:
        post.insert (9, {'author':'', 'body':'If you hold the comment button, you will see your 4 most used emoji'})
    # if len(post) > 15:
    #     post.insert (12, {'author':'', 'body':'The third name you see when you click Share then More secretly has a crush on you'})
    
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
            title_image(post[j].title, author, "r/"+subreddit)
            soundify_author(post[j].title, asker)
        else:
            # if not title post, create comment caption
            try:
                text = post[j].body
            except AttributeError:
                text = post[j]['body']

            sections = []

            # control size of caption to fit it on the screen vertically
            if len(text) > 450:
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
                            comment_blank_image(sections[section], j, asker)
                            soundify_comment(sections[section], j, section, asker)
                    except TypeError:
                        comment_image(author, sections[section], j, section, asker)
                        soundify_comment(sections[section], j, section, asker)

    # # create audio for title caption
    # soundifyAuthor(post[0].title, asker)

    if post[0].author is None:
        author = "[deleted]"
    else:
        author = post[0].author.name

    create_video(author)

if __name__ == '__main__':
    # input of how many posts to scrape
    num_of_posts = input('How many videos would you like to create?\n')
    while not num_of_posts.isnumeric():
        num_of_posts = input('That was not a number. How many videos would you like to create?\n')
    num_of_posts = int(num_of_posts)
    
    t1 = time.perf_counter()

    # threading/multiprocessing to speed up video creation
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(num_of_posts):
            print(f'Checking post #{i+1} criteria.')
            executor.submit(process_video, i)

    t2 = time.perf_counter()

    print(f'Finished in {t2-t1} seconds')

# TikTok tags :
# #fyp #foryoupage #askreddit #reddit #askredditstories #redditreadings #reddittts