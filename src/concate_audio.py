import argparse
from pydub import AudioSegment
import os
import natsort
import random

def combine_audio_files_directory(directory: str, output: str) -> AudioSegment:
    audio_files = [os.path.join(directory, f) for f in natsort.natsorted(os.listdir(directory)) if f.endswith('.wav')]
    combined_audio = AudioSegment.empty()
    for file in audio_files:
        audio = AudioSegment.from_file(file)
        combined_audio += audio
    combined_audio.export(output, format='wav')
    return combined_audio

def combine_audio_files_with_random_pause(directory, output) -> AudioSegment:
    combined_audio = AudioSegment.empty()
    audio_files = [os.path.join(directory, f) for f in natsort.natsorted(os.listdir(directory)) if f.endswith('.wav')]
    for i, file in enumerate(audio_files):
        audio = AudioSegment.from_file(file)
        if i > 0:
            pause_duration = random.randint(300, 500)
            combined_audio += AudioSegment.silent(duration=pause_duration)
        combined_audio += audio
    combined_audio.export(output, format='wav')
    return combined_audio

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Combine multiple audio files into one')
    parser.add_argument('files', metavar='FILE', nargs='+', help='list of audio files to combine')
    parser.add_argument('-o', '--output', default='combined_audio.wav', help='output filename (default: combined_audio.wav)')
    args = parser.parse_args()

    # call the combine_audio_files_directory function with the list of input files
    combined_audio = combine_audio_files_directory(args.files[0], args.output)

    # export the combined audio to the specified output file
    combined_audio.export(args.output, format='wav')
