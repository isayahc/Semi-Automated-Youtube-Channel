import os
import spacy

import src.utils.play_ht_api
import src.utils.reddit_api

if __name__ == '__main__':

    sample = r"\reddit\post"
    posts = src.utils.reddit_api.get_subreddit('dndstories')
    hot_posts = posts.top("all", limit=3)
    hot_posts = [*hot_posts]

    posts_dict_0 = [{"title": post.title, "body": post.selftext} for post in hot_posts]
    posts_dict = [{"title": src.utils.reddit_api.clean_up(post.title), "body": src.utils.reddit_api.clean_up(post.selftext)} for post in hot_posts]


    first_story = posts_dict[-1]

    story = temp = src.utils.reddit_api.turn_post_into_script(first_story['body'],first_story['title'])


    nlp = spacy.load("en_core_web_md")
    doc = nlp(story)

    doc_sents = [*doc.sents]

    doc_sents_text = data = [i.text for i in doc.sents]
    # data = join_sentences(doc_sents_text)

    directory = src.utils.reddit_api.create_next_dir(sample)

    for num,j in enumerate(data):
        src.utils.play_ht_api.generate_track_on_machine(j,f"story_part_{num}.wav",directory,speed="0.815")

    complete_audio = os.path.join(directory,"complete.wav")
    src.concate_audio.concate_audio.combine_audio_files_directory(directory,complete_audio)



    # dirs = [d for d in os.listdir(r"C:\Users\isaya\code_examples\Machine_Learning\wiki_data_set\reddit\post\") if os.path.isdir(d) and re.match(dir_pattern, d) ]

    
    
    
    src.reddit_apiget_subreddit('dndstories')

