import argparse
from pydub import AudioSegment
import os
import natsort

def combine_audio_files(audio_files):
    # initialize an empty AudioSegment object
    combined_audio = AudioSegment.empty()

    # loop through each audio file and append it to the combined_audio object
    for file in audio_files:
        audio = AudioSegment.from_file(file)
        combined_audio += audio

    # return the combined audio as a PyDub AudioSegment object
    return combined_audio

def combine_audio_files_directory(directory: str, output: str) -> AudioSegment:
    # Get a list of all the audio files in the directory

    audio_files = [os.path.join(directory, f) for f in natsort.natsorted(os.listdir(directory)) if f.endswith('.wav')]

    # Initialize an empty AudioSegment object
    combined_audio = AudioSegment.empty()

    # Loop through each audio file and append it to the combined_audio object
    for file in audio_files:
        audio = AudioSegment.from_file(file)
        combined_audio += audio

    # Save the combined audio to the specified output file
    combined_audio.export(output, format='wav')

    # Return the combined audio as a PyDub AudioSegment object
    return combined_audio

import random

def combine_audio_files_with_random_pause(directory, output):
    # Initialize an empty AudioSegment object
    combined_audio = AudioSegment.empty()

    # Get a list of all the audio files in the directory
    audio_files = [os.path.join(directory, f) for f in natsort.natsorted(os.listdir(directory)) if f.endswith('.wav')]

    # Loop through each audio file and append it to the combined_audio object
    for i, file in enumerate(audio_files):
        audio = AudioSegment.from_file(file)

        # Add a random pause between 300ms to 900ms after the first audio file
        if i > 0:
            pause_duration = random.randint(300, 500)
            combined_audio += AudioSegment.silent(duration=pause_duration)

        combined_audio += audio

    # Save the combined audio to the specified output file
    combined_audio.export(output, format='wav')

    # Return the combined audio as a PyDub AudioSegment object
    return combined_audio



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Combine multiple audio files into one')
    parser.add_argument('files', metavar='FILE', nargs='+', help='list of audio files to combine')
    parser.add_argument('-o', '--output', default='combined_audio.wav', help='output filename (default: combined_audio.wav)')
    args = parser.parse_args()

    # call the combine_audio_files function with the list of input files
    combined_audio = combine_audio_files(args.files)

    # export the combined audio to the specified output file
    combined_audio.export(args.output, format='wav')
