from typing import List, Tuple, Dict, Union
import re

import csv
from pydub import AudioSegment

import src.audio.concate_audio
from src.utils.play_ht_api import generate_track_on_machine
from src.utils.generate_subtitles import *
import src.utils.text_utils

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

def make_family_friendly(input_data:str,swear_bank:List[str],output_data:str="output0.wav"):
    x = transcribe_and_align(input_data)
    x_word_segments = x['word_segments']

    swear_word_segements = filter_text_by_list(x_word_segments,swear_bank)

    silence_segments(input_data, output_data, swear_word_segements)

def mask_swear_segments(word_list: List[str], x_word_segments: List[Dict[str, Union[str, float]]]) -> List[Dict[str, Union[str, float]]]:
    x_word_segments_copy = []
    for i in x_word_segments:
        segment_copy = i.copy()
        segment_copy['text'] = masked_words(word_list, i['text'])
        x_word_segments_copy.append(segment_copy)
    return x_word_segments_copy

def remove_swears(audio_script:str) ->str:
    links_dict = get_swear_bank()

    for word, replacement in links_dict.items():
        audio_script = audio_script.replace(word, replacement)

    return audio_script

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