import argparse
import os

# Local/application specific imports
from src.utils import utils
from src.audio import audio_utils

#TODO:
# remove hardcoded file related variables

def validate_args(args):
    """
    Validates the file path arguments.

    Args:
        args: The command line arguments.
    """
    if not os.path.isfile(args.audio_link):
        raise ValueError(f"File not found: {args.audio_link}")
    if not os.path.isfile(args.vid_link):
        raise ValueError(f"File not found: {args.vid_link}")


def main():
    """
    Main function to handle command line arguments and initiate the video generation.
    """
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

    # Validate the arguments
    validate_args(args)

    # If no swear word list is provided, default to the predefined list
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
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")