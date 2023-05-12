import os
import re
from typing import List, Tuple

import src.audio.concate_audio
from .play_ht_api import generate_track_on_machine
from .generate_subtitles import *


def replace_caps_with_hyphens(sentence):
    pattern = r'\b([A-Z]+)\b'
    replacement = lambda match: '-'.join(list(match.group(1)))
    return re.sub(pattern, replacement, sentence)


def remove_parenthesis(text:str):
    # define the pattern to match
    pattern = r'\(([^\s()]+)\)'
    # remove the tokens from the string using regular expressions
    # remove any text enclosed in parentheses if it contains only one word
    text_without_single_word_parentheses = re.sub(
        pattern, lambda m: m.group(1) if ' ' in m.group(1) else '', text
        )
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



def filter_text_by_list(text_list: List[Dict[str, Union[str, float]]], word_list: List[str]) -> List[Dict[str, Union[str, float]]]:
    '''returns segments of swear words'''
    filtered_list = []
    for item in text_list:
        # Remove all non-alphanumeric characters from the item's text
        cleaned_text = re.sub(r'[^a-zA-Z\d\s]', '', item['text'])
        if cleaned_text.lower() in word_list:
            filtered_list.append(item)
    return filtered_list
