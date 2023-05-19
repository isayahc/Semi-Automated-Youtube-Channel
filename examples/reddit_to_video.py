"""
This module fetches posts from a subreddit, converts one of the posts into audio,
then generates a video with subtitles from the audio and a sample video.
"""

import os
import sys
import logging
from dotenv import load_dotenv
from pathlib import Path

# Third party imports
from elevenlabs import set_api_key, generate, save

# Local/application specific imports
from src.utils import reddit_api, utils
from src.audio import audio_utils

def check_environment_variables():
    """
    Checks if necessary environment variables are set.
    
    This function gets the 'ELEVENLABS_API_KEY' and 'STRING_AUDIO_FILE_LOCATION' 
    from the environment variables and checks if they are set.
    
    Returns:
        ELEVENLABS_API_KEY (str): The API key for elevenlabs.
        STRING_AUDIO_FILE_LOCATION (str): The location to store the audio file.
        
    Raises:
        SystemExit: If the environment variables are not set.
    """
    ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
    if not ELEVENLABS_API_KEY:
        logging.error("The ELEVENLABS_API_KEY environment variable is not set.")
        sys.exit(1)

    STRING_AUDIO_FILE_LOCATION = os.getenv("STRING_AUDIO_FILE_LOCATION")
    if not STRING_AUDIO_FILE_LOCATION:
        logging.error("The STRING_AUDIO_FILE_LOCATION environment variable is not set.")
        sys.exit(1)

    return ELEVENLABS_API_KEY, STRING_AUDIO_FILE_LOCATION

# This function fetches posts from the specified subreddit
def fetch_reddit_posts(subreddit):
    return reddit_api.fetch_reddit_posts(subreddit)

# This function creates a directory in the specified location to store the audio file
def create_audio_directory(audio_file_location):
    audio_directory = utils.create_next_dir(audio_file_location)
    current_directory = os.getcwd()
    directory_path = os.path.join(current_directory, Path(audio_directory))
    return directory_path

# This function generates an audio file from the specified script using the Eleven Labs API
def generate_audio(script, voice, model):
    return generate(text=script, voice=voice, model=model)

def main(api_key, audio_file_location):
    subreddit = 'dndstories'

    # Fetch posts from the subreddit
    posts_dict = fetch_reddit_posts(subreddit)
    first_story = posts_dict[-1]

    # Convert the first post into a script
    script_first_story = reddit_api.turn_post_into_script(
        first_story['body'], first_story['title'])

    # Create a directory to store the audio file
    directory_path = create_audio_directory(audio_file_location)
    complete_audio_path = os.path.join(directory_path, "story_part_0.wav")

    # Fetch the list of swear words to filter
    swear_word_list = [*audio_utils.get_swear_word_list().keys()]

    # Generate the audio from the script
    audio = generate_audio(script_first_story, voice="Bella", model="eleven_monolingual_v1")
    save(audio, complete_audio_path)

    input_video_file = r'sample_video.mp4'
    output_video_file = r"sample_0.mp4"

    # Generate the final video with subtitles, filtering out any swear words
    utils.generate_video_with_subtitles(
        complete_audio_path, input_video_file, swear_word_list, output_video_file)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    load_dotenv()

    # Check environment variables and proceed if all necessary variables are set
    ELEVENLABS_API_KEY, STRING_AUDIO_FILE_LOCATION = check_environment_variables()
    set_api_key(ELEVENLABS_API_KEY)
    main(ELEVENLABS_API_KEY, STRING_AUDIO_FILE_LOCATION)
