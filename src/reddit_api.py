import praw
import re
import spacy
from typing import List, Tuple
from .play_ht_api import generate_track_on_machine
from .generate_subtitles import *
import csv
from pydub import AudioSegment
from pathlib import Path
import os
import src.concate_audio
import natsort
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')



def replace_caps_with_hyphens(sentence):
    pattern = r'\b([A-Z]+)\b'
    replacement = lambda match: '-'.join(list(match.group(1)))
    return re.sub(pattern, replacement, sentence)

def remove_parenthesis(text:str):
    # define the pattern to match
    pattern = r'\(([^\s()]+)\)'
    # remove the tokens from the string using regular expressions
    # remove any text enclosed in parentheses if it contains only one word
    text_without_single_word_parentheses = re.sub(pattern, lambda m: m.group(1) if ' ' in m.group(1) else '', text)
    # return text_without_tokens
    return text_without_single_word_parentheses
    

def replace_hyphens_with_single_space(text):
    return re.sub(r'-\B|\B-', ' ', text)

def add_spaces_around_hyphen(words):
    return re.sub(r'([a-zA-Z])-([a-zA-Z])', r'\1 - \2', words)

def add_spaces_around_hyphens(input_str):
    # Replace all hyphens with a space followed by a hyphen followed by another space
    # Example: 'A-I-T-A' -> 'A - I - T - A'
    output_str = re.sub(r'-', ' - ', input_str)
    
    return output_str

def clean_up(text:str) -> str:
    # text = text.replace("\n"," ")
    text = " ".join(text.split())

    text = remove_parenthesis(text)

    text = text.replace("\\"," slash ")

    if "r/" in text:
        text = text.replace("r/", " R slash ")

    if "AITA" in text:
        text = text.replace("AITA", " am i the asshole  ")


    text = replace_hyphens_with_single_space(text)
    text = replace_caps_with_hyphens(text)
    text =  add_spaces_around_hyphen(text)


    return text


def get_subreddit(sub:str):
    reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,         
    client_secret=REDDIT_CLIENT_SECRET,      
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)")

    # get the subreddit
    subreddit = reddit.subreddit(sub)
    return subreddit


def join_sentences(sentences: List[str]) -> List[str]:
    '''splits body of text such that it never surpases maximum token 250'''
    result = []
    current_sentence = ""
    current_word_count = 0
    
    for sentence in sentences:
        # split sentence into words and add to current word count
        words = sentence.split()
        current_word_count += len(words)
        
        # if adding the current sentence would result in too many words, add the current sentence to the result
        if current_word_count > 249:
            result.append(current_sentence)
            current_sentence = ""
            current_word_count = 0
        
        # add current sentence and a space to the result
        if len(current_sentence) > 0:
            current_sentence += " "
        
        # add current sentence to the result
        current_sentence += sentence
    
    # add final sentence to the result
    result.append(current_sentence)
    
    return result



def turn_post_into_script(reddit_post,reddit_title):
    ending = " . Ever been in a situation like this? Leave it in the comment section. Like and subscribe if you enjoyed this video and want to see more like them. Thank you for watching my video. I hope you enjoyed it, and please have a wonderful day."
    opening = f"Today's story from reddit - - ... {reddit_title} ... let's get into the story ... "

    total_script = opening + reddit_post + ending
    return total_script


def get_swear_bank():
        with open(r'C:\Users\isaya\code_examples\Machine_Learning\wiki_data_set\reddit\censor.csv', 'r') as f:
            reader = csv.reader(f)
            # create a dictionary with the first column as the keys and the second column as the values
            links_dict = {rows[0]: rows[1] for rows in reader}
        return links_dict


def masked_words(words_to_mask:List[str], string_to_mask:str):
    '''mask sear words'''
    for word in words_to_mask:
        pattern = r"\b{}\b".format(word)  # Create a regex pattern for the word
        # Replace the word with asterisks, leaving the first and last character unchanged
        string_to_mask = re.sub(pattern, lambda match: match.group(0)[0] + "*"*(len(match.group(0))-2) + match.group(0)[-1], string_to_mask, flags=re.IGNORECASE)
    return string_to_mask


def remove_swears(audio_script:str) ->str:
    links_dict = get_swear_bank()

    for word, replacement in links_dict.items():
        audio_script = audio_script.replace(word, replacement)

    return audio_script


def filter_text_by_list(text_list: List[Dict[str, Union[str, float]]], word_list: List[str]) -> List[Dict[str, Union[str, float]]]:
    '''returns segments of swear words'''
    filtered_list = []
    for item in text_list:
        # Remove all non-alphanumeric characters from the item's text
        cleaned_text = re.sub(r'[^a-zA-Z\d\s]', '', item['text'])
        if cleaned_text.lower() in word_list:
            filtered_list.append(item)
    return filtered_list


def silence_segments(input_file, output_file, segments):
    '''silences all selected segments'''
    # Load audio file
    audio = AudioSegment.from_file(input_file)

    # Loop over the list of segments
    for segment in segments:
        # Calculate the start and end times in milliseconds
        start_ms = segment['start'] * 1000
        end_ms = segment['end'] * 1000

        # Create a silent audio segment with the same duration as the specified segment
        duration = end_ms - start_ms
        silent_segment = AudioSegment.silent(duration=duration)

        # Replace the segment with the silent audio
        audio = audio[:start_ms] + silent_segment + audio[end_ms:]

    # Export the modified audio to a file
    audio.export(output_file, format="wav")


def mask_swear_segments(word_list: List[str], x_word_segments: List[Dict[str, Union[str, float]]]) -> List[Dict[str, Union[str, float]]]:
    x_word_segments_copy = []
    for i in x_word_segments:
        segment_copy = i.copy()
        segment_copy['text'] = masked_words(word_list, i['text'])
        x_word_segments_copy.append(segment_copy)
    return x_word_segments_copy



def make_family_friendly(input_data:str,swear_bank:List[str],output_data:str="output0.wav"):
    x = transcribe_and_align(input_data)
    x_word_segments = x['word_segments']

    swear_word_segements = filter_text_by_list(x_word_segments,swear_bank)

    silence_segments(input_data, output_data, swear_word_segements)

def create_next_dir(input_directory):
    dir_pattern = r'story_\d+'  # pattern to match directories
    dirs = [d for d in os.listdir(input_directory) if re.match(dir_pattern, d)]  # get list of directories matching pattern

    dirs = sorted_dirs = natsort.natsorted(dirs)
    if dirs:  # if there are matching directories
        last_dir = max(dirs)  # get the highest numbered directory
        next_num = int(re.search(r'\d+', last_dir).group()) + 1  # extract the number from the directory name and add 1
        new_dir = f'story_{next_num}'  # create the new directory name
    else:  # if there are no matching directories
        new_dir = 'story_1'  # start with directory number 1

    new_dir = os.path.join(input_directory,new_dir)

    os.makedirs(new_dir)  # create the new directory

    return new_dir

def create_next_dir(input_directory):
    dir_pattern = r'story_\d+'  # pattern to match directories
    dirs = [d for d in os.listdir(input_directory) if re.match(dir_pattern, d)]  # get list of directories matching pattern
    dirs = natsort.natsorted(dirs)  # sort the directories in natural order

    if dirs:  # if there are matching directories
        last_dir = dirs[-1]  # get the last directory in the sorted list
        next_num = int(re.search(r'\d+', last_dir).group()) + 1  # extract the number from the directory name and add 1
        new_dir = f'story_{next_num}'  # create the new directory name
    else:  # if there are no matching directories
        new_dir = 'story_1'  # start with directory number 1

    new_dir = os.path.join(input_directory, new_dir)

    os.makedirs(new_dir)  # create the new directory

    return new_dir

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

if __name__ == "__main__":

    input_data = r"C:\Users\isaya\code_examples\Machine_Learning\wiki_data_set\data_data_data_data_youtube.mp4"
    input_data = r"C:\Users\isaya\code_examples\Machine_Learning\wiki_data_set\big_swears.wav"

    sample = r"C:\Users\isaya\code_examples\Machine_Learning\wiki_data_set\reddit\post"
    


    # swear_bank = [*get_swear_bank().keys()]
    # masked_script = mask_swear_segments(input_data,swear_bank) 

    # make_family_friendly(input_data,swear_bank,"output0.wav")

 
    # posts = get_subreddit('pettyrevenge')

    posts = get_subreddit('askreddit')

    

    hot_posts = posts.top("all", limit=3)
    hot_posts = [*hot_posts]


    reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,         
    client_secret=REDDIT_CLIENT_SECRET,      
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)")

    url = "https://www.reddit.com/r/AskReddit/comments/11h681p/whats_an_unwritten_rule_about_the_road_that_new/"
    submission = reddit.submission(url=url)
    comments = submission.comments.list()

    # get the subreddit
    # subreddit = reddit.subreddit(sub)
    # res = get_all(reddit, "6rjwo1", verbose=False) 

    # get_all(res,)


    posts_dict = [{"title": clean_up(post.title), "body": clean_up(post.selftext)} for post in hot_posts]

    # sample code
    first_story = posts_dict[-1]

    story = temp = turn_post_into_script(first_story['body'],first_story['title'])


    nlp = spacy.load("en_core_web_md")
    doc = nlp(story)

    doc_sents = [*doc.sents]

    doc_sents_text = data = [i.text for i in doc.sents]
    # data = join_sentences(doc_sents_text)

    directory = create_next_dir(sample)

    for num,j in enumerate(data):
        generate_track_on_machine(j,f"story_part_{num}.wav",directory,speed="0.815")

    complete_audio = os.path.join(directory,"complete.wav")
    src.concate_audio.concate_audio.combine_audio_files_directory(directory,complete_audio)



    # dirs = [d for d in os.listdir(r"C:\Users\isaya\code_examples\Machine_Learning\wiki_data_set\reddit\post\") if os.path.isdir(d) and re.match(dir_pattern, d) ]
