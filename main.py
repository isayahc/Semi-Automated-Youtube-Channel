import os

import argparse

# Third party imports
from elevenlabs import set_api_key, generate, save

# Local/application specific imports
from src.utils import utils
from src.audio import audio_utils

#TODO:
# add srt. optional output location
# handle temp files created by function
# remove hardcoded file related variables

def main():
    parser = argparse.ArgumentParser(description='Generate video with subtitles.')
    parser.add_argument('--audio_link', type=str, required=True,
                        help='Path to the audio file.')
    parser.add_argument('--vid_link', type=str, required=True,
                        help='Path to the video file.')
    parser.add_argument('--swear_word_list', nargs='+', required=False, default=[],
                        help='List of swear words to be filtered out.')
    parser.add_argument('--video_output', type=str, required=True,
                        help='Path for the output video file.')
    parser.add_argument('--srtFilename', type=str, required=False, default="",
                        help='Path for the subtitle file. If not provided, no subtitle file will be saved.')
    
    args = parser.parse_args()

    if not args.swear_word_list:
        args.swear_word_list = audio_utils.get_swear_word_list().keys()

    utils.generate_video_with_subtitles(
        args.audio_link, 
        args.vid_link, 
        args.swear_word_list, 
        args.video_output,
        args.srtFilename
        )


    
if __name__ == '__main__':
    ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
    if not ELEVENLABS_API_KEY:
        print("Error: The ELEVENLABS_API_KEY environment variable is not set.")
        exit(1)
    STRING_AUDIO_FILE_LOCATION = os.getenv("STRING_AUDIO_FILE_LOCATION")
    if not STRING_AUDIO_FILE_LOCATION:
        print("Error: The STRING_AUDIO_FILE_LOCATION environment variable is not set.")
        exit(1)
    set_api_key(ELEVENLABS_API_KEY)
    main()
