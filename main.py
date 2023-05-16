import os
from pathlib import Path

import spacy
from elevenlabs import set_api_key, generate, save

import src.utils.play_ht_api
import src.utils.reddit_api
import src.utils.text_utils
import src.utils.generate_subtitles
import src.utils.utils
import src.audio.concate_audio


#configuring elenlabs functionality
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
#location of where the .wav files will be stored
# Access the environment variable
STRING_AUDIO_FILE_LOCATION = os.getenv("STRING_AUDIO_FILE_LOCATION")
set_api_key(ELEVENLABS_API_KEY)

if __name__ == '__main__':
    #gets the data from a selected subreddit
    reddit_subreddit = src.utils.reddit_api.get_subreddit('dndstories')

    #queries the 3 post popular post of a given subreddit
    hot_subreddit_posts = reddit_subreddit.top("all", limit=3)
    hot_subreddit_posts = [*hot_subreddit_posts]

    posts_dict = [{"title": src.utils.text_utils.clean_up(post.title), "body": src.utils.text_utils.clean_up(post.selftext)} for post in hot_subreddit_posts]

    # chooses the first reddit story in the query
    first_story = posts_dict[-1]

    #turns the selected reddit story into a simple youtube script
    script_first_story = src.utils.reddit_api.turn_post_into_script(
        first_story['body'],
        first_story['title']
        )

    #initializes the spacy model
    nlp = spacy.load("en_core_web_md")
    doc = nlp(script_first_story)

    #seperates the reddit story into individual stories
    doc_sents = [*doc.sents]

    doc_sents_text = data = [i.text for i in doc.sents]

    # will create a directory in a given location story_n
    # where n is the number of directories with the name story
    audio_directory = src.utils.utils.create_next_dir(STRING_AUDIO_FILE_LOCATION)

    current_directory = os.getcwd()
    # Create the directory in the current working directory
    directory_path = os.path.join(current_directory, Path(audio_directory))

    # breaks the entire text into chunks to be joined latter on
    for num,data in enumerate(doc_sents_text):

        audio = generate(
        text=data,
        voice="Bella",
        model="eleven_monolingual_v1"
        )

        save(audio, os.path.join(audio_directory,f"story_part_{num}.wav"))


    # location of where the concated audio files will be stored as a single .wav file
    complete_audio = os.path.join(audio_directory,"complete.wav")

    # concatinate all the videos in a directory
    src.audio.concate_audio.combine_audio_files_directory(audio_directory)

    # Use whisper to provide subtitles
    complete_audio_blank = src.utils.generate_subtitles.transcribe_and_align(complete_audio)

    complete_audio_blank_segments = complete_audio_blank['word_segments']

    subtitltes = src.utils.generate_subtitles.segment_text_by_word_length(complete_audio_blank_segments)

    
    # Add the subtitles to the video
    # s = src.utils.generate_subtitles.add_subtitles_to_video(input_path, output_path, subtitles)
