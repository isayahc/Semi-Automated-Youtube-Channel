import os
import subprocess
import re
from typing import List

from datetime import timedelta
from pathlib import Path
import argparse
import natsort


from audio.concate_audio import combine_audio_files
import audio.audio_utils
from video.random_sample_clip import create_clip_with_matching_audio
from generate_subtitles import add_subtitles_to_video, transcribe_and_align, segment_text_by_word_length

def combine_audio_and_video(video_path: str, audio_path: str, output_path: str) -> None:
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

def generate_video(uncensored_audio_file: str, source_video: str, swear_bank: List[str], out_put_location: str, whisper_model: str = "medium") -> None:
    """
    Generate a censored video with masked audio and subtitles.

    Args:
        uncensored_audio_file (str): The path to the uncensored audio file.
        source_video (str): The path to the source video file.
        swear_bank (List[str]): A list of swear words to be censored.
        out_put_location (str): The path to save the generated video.
        whisper_model (str, optional): The Whisper ASR model type. Defaults to "medium".

    Returns:
        None
    """
    swear_bank = [*reddit_api.get_swear_bank().keys()]

    raw_transcript = transcribe_and_align(uncensored_audio_file,model_type=whisper_model) #complete script
    parent_folder = os.path.dirname(out_put_location)

    segments = raw_transcript['segments']
    segments = reddit_api.mask_swear_segments(swear_bank,segments)
    
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



    raw_word_segments = masked_word_segment = raw_transcript['word_segments']

    masked_script = reddit_api.mask_swear_segments(swear_bank,raw_word_segments) #adds mask to existing script

    swear_segments = reddit_api.filter_text_by_list(raw_word_segments,swear_bank)

    n_segment = segment_text_by_word_length(masked_script,)

    video_clip = Path("sample.mp4")

    family_friendly_audio = Path(uncensored_audio_file).with_name("uncensored.wav")


    reddit_api.silence_segments(uncensored_audio_file,str(family_friendly_audio),swear_segments)

    create_clip_with_matching_audio(source_video,str(family_friendly_audio),str(video_clip))


    add_subtitles_to_video(str(video_clip),out_put_location,n_segment)

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
if __name__ == "__main__":
    swear_bank = [*audio.audio_utils.get_swear_bank().keys()]
    parser = argparse.ArgumentParser()
    parser.add_argument("uncensored_audio_file", type=str, help="Path to the uncensored audio file")
    parser.add_argument("source_video", type=str, help="Path to the source video file")
    parser.add_argument("out_put_location", type=str, help="Path to the output video file")
    parser.add_argument("--swear_bank", type=str, nargs="+", help="List of swear words to mask", default=swear_bank)
    args = parser.parse_args()

    generate_video(args.uncensored_audio_file, args.source_video, args.swear_bank, args.out_put_location)