import os
from typing import List, Tuple
from dotenv import load_dotenv
from pathlib import Path

import praw

from .play_ht_api import generate_track_on_machine
from .generate_subtitles import *


# Load the .env file
load_dotenv()

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')


def get_subreddit(sub:str):
    reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,         
    client_secret=REDDIT_CLIENT_SECRET,      
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)")

    # get the subreddit
    subreddit = reddit.subreddit(sub)
    return subreddit


def turn_post_into_script(reddit_post,reddit_title):
    ending = " . Ever been in a situation like this? Leave it in the comment section. Like and subscribe if you enjoyed this video and want to see more like them. Thank you for watching my video. I hope you enjoyed it, and please have a wonderful day."
    opening = f"Today's story from reddit - - ... {reddit_title} ... let's get into the story ... "

    total_script = opening + reddit_post + ending
    return total_script


def get_sub_comments(comment, allComments, verbose=True):
    allComments.append(comment)
    if not hasattr(comment, "replies"):
        replies = comment.comments()
        if verbose: print("fetching (" + str(len(allComments)) + " comments fetched total)")

        else:
            replies = comment.replies
        for child in replies:
            get_sub_comments(child, allComments, verbose=verbose)

def get_all(r, submissionId, verbose=True):
    submission = r.submission(submissionId)
    comments = submission.comments
    commentsList = []
    for comment in comments:
        get_sub_comments(comment, commentsList, verbose=verbose)
        return commentsList

