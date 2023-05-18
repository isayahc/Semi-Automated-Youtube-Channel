import os
import subprocess
import re
from typing import List

from datetime import timedelta
from pathlib import Path
import argparse

from src.video import random_sample_clip
from src.utils import generate_subtitles, text_utils
from src.audio import audio_utils


def combine_audio_and_video(
        video_path: str, 
        audio_path: str, 
        output_path: str) -> None:
    """
    Combine the given audio and video files into a single output video file.

    Args:
        video_path (str): The path to the input video file.
        audio_path (str): The path to the input audio file.
        output_path (str): The path to save the combined output video file.

    Returns:
        None
    """

    ffmpeg_cmd = [
        "ffmpeg",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-map", "0:v:0",
        "-map", "1:a:0",
        output_path,
        "-y"
    ]
    
    subprocess.run(ffmpeg_cmd, check=True)

def generate_video_with_subtitles(
        uncensored_audio_file: str, 
        source_video: str, 
        swear_word_list: List[str], 
        video_output_location: str, 
        whisper_model: str = "medium") -> None:
    """
    Generate a censored video with masked audio and subtitles.

    Args:
        uncensored_audio_file (str): The path to the uncensored audio file.
        source_video (str): The path to the source video file.
        swear_word_list (List[str]): A list of swear words to be censored.
        video_output_location (str): The path to save the generated video.
        whisper_model (str, optional): The Whisper ASR model type. Defaults to "medium".

    Returns:
        None
    """
    swear_word_list = [*audio_utils.get_swear_word_list().keys()]

    raw_transcript = generate_subtitles.transcribe_and_align(
        uncensored_audio_file,
        model_type=whisper_model
        ) #complete script
    
    parent_folder = os.path.dirname(video_output_location)

    segments = raw_transcript['segments']
    segments = audio_utils.mask_swear_segments(swear_word_list,segments)
    
    srtFilename = os.path.join(parent_folder, f"VIDEO_FILENAME.srt")
    if os.path.exists(srtFilename):
        os.remove(srtFilename)

    for (i,segment) in enumerate(segments):
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']

        segment = f"{i}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"
        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)


    raw_word_segments  = raw_transcript['word_segments']

    masked_script = audio_utils.mask_swear_segments(swear_word_list,raw_word_segments) #adds mask to existing script

    swear_segments = text_utils.filter_text_by_list(raw_word_segments,swear_word_list)
    

    n_segment = generate_subtitles.segment_text_by_word_length(masked_script,)

    video_clip = Path("sample.mp4")

    family_friendly_audio = Path(uncensored_audio_file).with_name("uncensored.wav")


    audio_utils.silence_segments(
        uncensored_audio_file,
        str(family_friendly_audio),
        swear_segments
        )
    
    random_sample_clip.create_clip_with_matching_audio(
        source_video,
        str(family_friendly_audio),
        str(video_clip)
        )

    generate_subtitles.add_subtitles_to_video(
        str(video_clip),
        video_output_location,
        n_segment
        )


def create_next_dir(input_directory: str) -> str:
    input_directory = Path(input_directory)
    is_absolute = input_directory.is_absolute()

    # pattern to match directories
    dir_pattern = r'story_\d+'

    current_directory = Path(os.getcwd())
    if not is_absolute:
        directory_path = Path.joinpath(current_directory, input_directory)
        if directory_path.exists():
            dirs = [d for d in os.listdir(directory_path) if re.match(dir_pattern, d)]
            # extract the numbers from the directory names and convert them to integers
            dir_numbers = [int(re.search(r'\d+', d).group()) for d in dirs]
            # get the maximum number
            next_num = max(dir_numbers) + 1
            # create the new directory name
            new_dir = f'story_{next_num}'
            directory_path = Path.joinpath(current_directory, input_directory, Path(new_dir))

        else:
            directory_path = Path.joinpath(current_directory, input_directory, Path('story_1'))

    os.makedirs(directory_path)

    return directory_path


if __name__ == "__main__":
    # swear_word_list = [*audio.audio_utils.get_swear_word_list().keys()]
    swear_word_list = []
    parser = argparse.ArgumentParser()
    parser.add_argument("uncensored_audio_file", type=str, help="Path to the uncensored audio file")
    parser.add_argument("source_video", type=str, help="Path to the source video file")
    parser.add_argument("video_output_location", type=str, help="Path to the output video file")
    parser.add_argument("--swear_word_list", type=str, nargs="+", help="List of swear words to mask", default=swear_word_list)
    args = parser.parse_args()

    generate_video_with_subtitles(args.uncensored_audio_file, args.source_video, args.swear_word_list, args.video_output_location)