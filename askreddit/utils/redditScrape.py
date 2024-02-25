import praw
import os
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit (
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')

)

def get_posts(sub, count, span):
    subreddit = reddit.subreddit(sub)
    posts = []
    for submission in subreddit.top(span, limit=count):
        if "r/" not in submission.title and "reddit" not in submission.title:
            posts.append(submission)

    return posts

def get_comments(submission):
    submission.comment_sort = 'best'

    comments = []
    num_comments = 30

    for top_level_comment in submission.comments:
        
        # make sure it's not a link or removed and get top #num comments
        try:
            if "http" not in top_level_comment.body and len(comments) <= num_comments and top_level_comment.body != ('[removed]' or '[deleted]'):
                comments.append(top_level_comment)
            elif len(comments) > num_comments:
                break
        except AttributeError:
            pass

    return comments

def scrapeComments(subreddit, count, span):
    posts = get_posts(subreddit, count, span)
    

    for post in posts:
        got_comments = get_comments(post)

        for comment in got_comments:
            if len(comment.body) > 600:
                got_comments = [comment]
                break
        comments=[post]
        length = 0
        # return as many comments that are under 2000 characters
        for comment in range(len(got_comments)):
            length += len(got_comments[comment].body)
            if length > 2000 and comment > 0:
                break
            else:
                comments.append(got_comments[comment])
        # for comment in range(len(got_comments)):
        #     length += len(got_comments[comment].body)
        #     if length < 3000:
        #         comments.append(got_comments[comment])

    return comments

if __name__ == "__main__":
    scrapeComments("askreddit", 1, "day")
