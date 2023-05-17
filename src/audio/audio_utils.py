from typing import List, Tuple, Dict, Union
import re
import os

import csv
from pydub import AudioSegment

from src.audio import concate_audio
from src.utils import (generate_subtitles, text_utils)
from src.utils.generate_subtitles import *


SWEAR_WORD_LIST_FILE_LOCATION = os.getenv('SWEAR_WORD_LIST_FILE_LOCATION_FILE_LOCATION')

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

def make_family_friendly(input_data:str,swear_word_list:List[str],output_data:str="output0.wav"):
    x = transcribe_and_align(input_data)
    x_word_segments = x['word_segments']

    swear_word_segements = text_utils.filter_text_by_list(x_word_segments,swear_word_list)

    silence_segments(input_data, output_data, swear_word_segements)

def mask_swear_segments(word_list: List[str], x_word_segments: List[Dict[str, Union[str, float]]]) -> List[Dict[str, Union[str, float]]]:
    x_word_segments_copy = []
    for i in x_word_segments:
        segment_copy = i.copy()
        segment_copy['text'] = mask_specific_words(word_list, i['text'])
        x_word_segments_copy.append(segment_copy)
    return x_word_segments_copy

def remove_swears(audio_script:str) ->str:
    links_dict = get_swear_word_list()

    for word, replacement in links_dict.items():
        audio_script = audio_script.replace(word, replacement)

    return audio_script

def get_swear_word_list():
        with open(SWEAR_WORD_LIST_FILE_LOCATION, 'r') as f:
            reader = csv.reader(f)
            # create a dictionary with the first column as the keys and the second column as the values
            links_dict = {rows[0]: rows[1] for rows in reader}
        return links_dict

def mask_word(match):
    word = match.group(0)
    return word[0] + "*" * (len(word) - 2) + word[-1]

def mask_specific_words(words_to_mask: List[str], string_to_mask: str) -> str:
    """
    Mask specific words in a given string by replacing them with asterisks, while preserving the first and last characters.

    Args:
        words_to_mask (List[str]): List of words to mask.
        string_to_mask (str): String to be masked.

    Returns:
        str: Masked string.
    """
    # Create a set of unique words to mask for faster lookup
    words_set = set(words_to_mask)

    # Compile the regex pattern to match any of the words to mask
    pattern = re.compile(r"\b(?:{})\b".format("|".join(re.escape(word) for word in words_set)), flags=re.IGNORECASE)

    # Replace the matched words with asterisks, preserving the first and last characters

    # Perform the replacement using the compiled pattern and mask_word function
    masked_string = pattern.sub(mask_word, string_to_mask)

    return masked_string