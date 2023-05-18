import os
import subprocess
import re
from typing import List, Dict, Any

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

    parent_folder = os.path.dirname(video_output_location)
    srtFilename = os.path.join(parent_folder, f"VIDEO_FILENAME.srt")
    video_clip = Path("sample.mp4")
    family_friendly_audio = Path(uncensored_audio_file).with_name("uncensored.wav")
    
    #complete script generated from audio file

    raw_transcript = generate_subtitles.transcribe_and_align(
        uncensored_audio_file,
        model_type=whisper_model
        )
    

    segments = raw_transcript['segments']

    segments = audio_utils.mask_swear_segments(
        swear_word_list,
        segments
        )
    
    
    if os.path.exists(srtFilename):
        os.remove(srtFilename)

    #generate srt file from segments
    write_srt_file(segments, srtFilename)

    raw_word_segments  = raw_transcript['word_segments']

    #adds mask to existing script
    masked_script = audio_utils.mask_swear_segments(
        swear_word_list,
        raw_word_segments
        )

    
    #find times when the speaker swears
    swear_segments = text_utils.filter_text_by_list(
        raw_word_segments,
        swear_word_list
        )
    

    n_segment = generate_subtitles.segment_text_by_word_length(masked_script,)


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
    
    #remove temp files
    os.remove(video_clip)
    os.remove(family_friendly_audio)


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

def write_srt_file(segments: List[Dict[str, Any]], srt_filename: str) -> None:
    """
    Write an SRT file from a list of video segments.

    This function writes the given segments into an SRT (SubRip Text) file,
    which is a common format for subtitles. Each segment includes start and end times
    and the associated text.

    Args:
        segments: A list of dictionaries representing video segments, where each
                  dictionary includes 'start', 'end', and 'text' keys.
        srt_filename: The filename for the resulting SRT file.

    Returns:
        None
    """

    for i, segment in enumerate(segments):
        # Convert start and end times to SRT time format (hh:mm:ss,ms)
        start_time = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        end_time = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'

        # Get the text associated with this segment
        text = segment['text']

        # Create the SRT-formatted string for this segment
        srt_segment = f"{i+1}\n{start_time} --> {end_time}\n{text[1:] if text[0] == ' ' else text}\n\n"

        # Append this segment to the SRT file
        with open(srt_filename, 'a', encoding='utf-8') as srt_file:
            srt_file.write(srt_segment)


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