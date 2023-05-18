import os
from pathlib import Path


# Third party imports
from elevenlabs import set_api_key, generate, save

# Local/application specific imports
from src.utils import reddit_api, utils
from src.audio import  audio_utils



def main():
    #gets the data from a selected subreddit
    #queries the 3 post popular post of a given subreddit
    subreddit = 'dndstories'
    posts_dict = reddit_api.fetch_reddit_posts(subreddit)

    # chooses the first reddit story in the query
    first_story = posts_dict[-1]

    #turns the selected reddit story into a simple youtube script
    script_first_story = reddit_api.turn_post_into_script(
        first_story['body'],
        first_story['title']
        )
    
    
    # will create a directory in a given location story_n
    # where n is the number of directories with the name story
    audio_directory = utils.create_next_dir(STRING_AUDIO_FILE_LOCATION)

    current_directory = os.getcwd()
    # Create the directory in the current working directory
    directory_path = os.path.join(current_directory, Path(audio_directory))

    complete_audio = os.path.join(audio_directory,f"story_part_0.wav")

    swear_word_list = [*audio_utils.get_swear_word_list().keys()]


    audio = generate(
        text=script_first_story,
        voice="Bella",
        model="eleven_monolingual_v1"
        )
    save(audio, complete_audio)
    
    vid_link = r'sample_video.mp4'

    video_output = r"sample_0.mp4"

    utils.generate_video_with_subtitles(complete_audio,vid_link,swear_word_list,video_output)

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
