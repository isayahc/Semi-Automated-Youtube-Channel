from concate_audio import combine_audio_files
from random_sample_clip import create_clip_with_matching_audio
from generate_subtitles import add_subtitles_to_video, transcribe_and_align, segment_text_by_word_length
import argparse
import subprocess
import reddit_api
from typing import List
from pathlib import Path
from datetime import timedelta
import os

def combine_audio_and_video(video_path, audio_path, output_path):
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

def generate_video(uncensored_audio_file:str,source_video:str,swear_bank:List[str],out_put_location,whisper_model="medium"):
    ''''''
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

    # for segment in segments:
    #     startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
    #     endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
    #     text = segment['text']
        # text = reddit_api1.mask_swear_segments(swear_bank,text,) 

        # segment = f"\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"
       
        

        # with open(srtFilename, 'a', encoding='utf-8') as srtFile:
        #     srtFile.write(segment)

    raw_word_segments = masked_word_segment = raw_transcript['word_segments']

    masked_script = reddit_api.mask_swear_segments(swear_bank,raw_word_segments) #adds mask to existing script

    swear_segments = reddit_api.filter_text_by_list(raw_word_segments,swear_bank)

    n_segment = segment_text_by_word_length(masked_script,)

    video_clip = Path("sample.mp4")

    family_friendly_audio = Path(uncensored_audio_file).with_name("uncensored.wav")


    reddit_api.silence_segments(uncensored_audio_file,str(family_friendly_audio),swear_segments)

    create_clip_with_matching_audio(source_video,str(family_friendly_audio),str(video_clip))


    # combine_audio_and_video(str(video_clip),str(family_friendly_audio),str(out_put_location))

    add_subtitles_to_video(str(video_clip),out_put_location,n_segment)


# if __name__ == '__main__':
#     swear_bank = [*reddit_api1.get_swear_bank().keys()]

#     audio_file = r"c:\Users\isaya\code_examples\Machine_Learning\wiki_data_set\big_swears.wav"
#     video_file = r"C:\Users\isaya\code_examples\Machine_Learning\wiki_data_set\car_clip.webm"
#     output_file = "cool.mp4"

#     audio_file = r"C:\Users\isaya\code_examples\Machine_Learning\wiki_data_set\reddit\post\story_1\complete.wav"
#     output_file = r"C:\Users\isaya\code_examples\Machine_Learning\wiki_data_set\reddit\post\story_1\cool.mp4"

#     source_video = r" c:\Users\isaya\code_examples\Machine_Learning\wiki_data_set\video_sources\Can_5_Valorant_Pros_Beat_5_Siege_Pros_In_Rainbow_Six_Siege.webm"

#     video_file = r"video_sources\Can_5_Valorant_Pros_Beat_5_Siege_Pros_In_Rainbow_Six_Siege.webm"
#     audio_file = r"c:\Users\isaya\code_examples\Machine_Learning\wiki_data_set\reddit\post\story_13\complete.wav"
#     output_file = r"c:\Users\isaya\code_examples\Machine_Learning\wiki_data_set\reddit\post\story_13\complete.mp4"


    
if __name__ == "__main__":
    swear_bank = [*reddit_api.get_swear_bank().keys()]
    parser = argparse.ArgumentParser()
    parser.add_argument("uncensored_audio_file", type=str, help="Path to the uncensored audio file")
    parser.add_argument("source_video", type=str, help="Path to the source video file")
    parser.add_argument("out_put_location", type=str, help="Path to the output video file")
    parser.add_argument("--swear_bank", type=str, nargs="+", help="List of swear words to mask", default=swear_bank)
    args = parser.parse_args()

    

    generate_video(args.uncensored_audio_file, args.source_video, args.swear_bank, args.out_put_location)


    # generate_video(audio_file,
    # video_file,
    # swear_bank,
    # output_file)


    # parser = argparse.ArgumentParser(description='Combine multiple audio files into one')
    # parser.add_argument('files', metavar='FILE', nargs='+', help='list of audio files to combine')
    # parser.add_argument('-ao', '--audio_output', default='combined_audio.wav', help='output filename (default: combined_audio.wav)')
    # parser.add_argument('-s', '--video_source', default='car_clip.webm', help='video source to edit from')
    # parser.add_argument("-fo",'--final_output', default='video_snippet.mp4', help='video source to edit from')
    # args = parser.parse_args()

    # call the combine_audio_files function with the list of input files

    # combined_audio = combine_audio_files(args.files)

    # # export the combined audio to the specified output file
    # combined_audio.export(args.audio_output, format='wav')


    # swear_bank = [*reddit_api1.get_swear_bank().keys()]
    # masked_script = reddit_api1.mask_swear_segements(args.audio_output,swear_bank)


    # create_clip_with_matching_audio(args.video_source,args.audio_output,"temp_video_audio.mp4")
    # combine_audio_and_video("temp_video_audio.mp4",args.audio_output,"temp_no_subs.mp4")
    # add_subtitles_to_video("temp_no_subs.mp4","temp_no_subs.mp4",masked_script)