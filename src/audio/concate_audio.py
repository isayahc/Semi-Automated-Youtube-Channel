#!/usr/bin/env python3

import os
import random
import sys
import argparse
from typing import List
from natsort import natsorted
from pydub import AudioSegment


def get_sorted_audio_files(directory: str) -> List[str]:
    return [os.path.join(directory, f) for f in natsorted(os.listdir(directory)) if f.endswith('.wav')]


def combine_audio_files_directory(directory: str, output: str) -> AudioSegment:
    """
    Combines all .wav audio files in a given directory into a single audio file and exports it to the specified output file.

    :param directory: Path to the directory containing the audio files to be combined.
    :param output: Path to the output file where the combined audio will be saved.
    :return: The combined audio as a PyDub AudioSegment object.
    """
    audio_files = get_sorted_audio_files(directory)
    combined_audio = AudioSegment.empty()
    for audio_file in audio_files:
        audio = AudioSegment.from_file(audio_file)
        combined_audio += audio
    combined_audio.export(output, format='wav')
    return combined_audio


def combine_audio_files_with_random_pause(directory:str, output:str) -> AudioSegment:
    """
    Combines all .wav audio files in a given directory into a single audio file with a random pause (300ms to 500ms) between
    each file and exports it to the specified output file.
    
    :param directory: Path to the directory containing the audio files to be combined.
    :param output: Path to the output file where the combined audio will be saved.
    :return: The combined audio as a PyDub AudioSegment object.
    """
    combined_audio = AudioSegment.empty()
    audio_files = get_sorted_audio_files(directory)
    combined_audio = AudioSegment.from_file(audio_files[0])
    for audio_file in audio_files[1:]:
        pause_duration = random.randint(300, 500)
        combined_audio += AudioSegment.silent(duration=pause_duration)
        audio = AudioSegment.from_file(audio_file)
        combined_audio += audio
    combined_audio.export(output, format='wav')
    return combined_audio


def main(args: List[str]) -> None:
    parser = argparse.ArgumentParser(description='Combine multiple audio files into one')
    parser.add_argument('directory', metavar='DIRECTORY', help='directory containing the audio files to combine')
    parser.add_argument('-o', '--output', default='combined_audio.wav', help='output filename (default: combined_audio.wav)')
    parser.add_argument('--pause', action='store_true', help='add random pause between files')
    args = parser.parse_args(args)

    if args.pause:
        combine_audio_files_with_random_pause(args.directory, args.output)
    else:
        combine_audio_files_directory(args.directory, args.output)



if __name__ == '__main__':
    main(sys.argv[1:])
