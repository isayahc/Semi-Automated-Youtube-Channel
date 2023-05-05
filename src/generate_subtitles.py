import moviepy.editor as mp
from pathlib import Path
import whisperx
import whisper
import pandas as pd
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import VideoFileClip
import argparse
from typing import List, Dict, Union, Tuple


def transcribe_and_align(input_path: Path, device: str = "cpu", model_type: str = "medium") -> dict:
    """Transcribe and align audio file.

    Args:
        input_path (Path): Path to audio file.
        device (str, optional): Device to use for transcription and alignment.
            Defaults to "cpu".
        model_type (str, optional): Type of model to use for transcription.
            Defaults to "medium".

    Returns:
        dict: Aligned transcriptions.
    """
    model = whisperx.load_model(model_type,device)
    result = model.transcribe(input_path)
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result_aligned = whisperx.align(result["segments"], model_a, metadata, input_path, device)
    return result_aligned


def segment_text_by_word_length(my_list: List[Dict[str, Union[str, float]]], word_length_max: int = 5) -> List[Dict[str, Union[str, float]]]:
    """
    Segments a list of dictionaries containing text and timestamps into groups of a specified maximum word length.
    
    Args:
        my_list (List[Dict[str, Union[str, float]]]): A list of dictionaries containing 'text', 'start', and 'end' keys.
        word_length_max (int, optional): The maximum number of words per segment. Defaults to 5.

    Returns:
        List[Dict[str, Union[str, float]]]: A list of dictionaries containing the segmented text and corresponding start and end timestamps.
    """
    segmented_text = []
    temp_segment = []

    for item in my_list:
        temp_segment.append(item)
        if len(temp_segment) == word_length_max:
            segmented_text.append(temp_segment)
            temp_segment = []

    if temp_segment:
        segmented_text.append(temp_segment)

    complete_segments = []
    for segment in segmented_text:
        start_time = segment[0]['start']
        end_time = segment[-1]['end']
        text = " ".join(item['text'] for item in segment)
        complete_segments.append({"text": text, "start": start_time, "end": end_time})

    return complete_segments

def get_video_size(filename: str) -> Tuple[int, int]:
    """
    Get the dimensions (width and height) of a video file.

    Args:
        filename (str): The path to the video file.

    Returns:
        Tuple[int, int]: A tuple containing the width and height of the video, in the format (width, height).
    """
    video = VideoFileClip(filename)
    return (video.w, video.h)


def add_subtitles_to_video(input_path: str, output_path: str, word_segments: list) -> None:
    """
    Add subtitles to a video file based on word segments with start and end times.

    Args:
        input_path (str): The path to the input video file.
        output_path (str): The path to the output video file with subtitles added.
        word_segments (list): A list of dictionaries containing 'text', 'start', and 'end' keys for each word segment.

    Returns:
        None
    """
    text_clip_data = {
        'start': [segment['start'] for segment in word_segments],
        'end': [segment['end'] for segment in word_segments],
        'text': [segment['text'] for segment in word_segments]
        }

    df = pd.DataFrame.from_dict(text_clip_data)

    movie_width, movie_height = get_video_size(input_path)
    # Write the video file
    video = VideoFileClip(input_path)
    generator = lambda txt: mp.TextClip(txt, fontsize=80, color='black', align='center', font='P052-Bold', stroke_width=3, bg_color="white",method='caption',size=(movie_width, movie_height))
    generator = lambda txt: mp.TextClip(txt, fontsize=80, color='white', align='center', font='P052-Bold', stroke_width=3, method='caption',size=(movie_width/2, movie_height),stroke_color="black",)
    subs = tuple(zip(tuple(zip(df['start'].values, df['end'].values)), df['text'].values))
    subtitles = SubtitlesClip(subs, generator,)


    final_clip = mp.CompositeVideoClip([video, subtitles.set_pos(('center','center')),])

    try:
        final_clip.write_videofile(output_path, fps=24)
    except OSError:
        Path(output_path).unlink()
        final_clip.write_videofile(output_path, fps=24)
        
    return output_path


def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Create a webm video using an input image and audio.")
    parser.add_argument("input_path", type=Path, help="Path to the input audio file.")
    parser.add_argument("output_path",  type=Path, default=None, help="Path to the output video file. If not provided, the input path will be used with a different file extension.")
    parser.add_argument("--device", type=str, default="cpu", help="Device to use for transcription and alignment (default: 'cpu')")
    parser.add_argument("--model_type", type=str, default="medium", help="Type of model to use for transcription (default: 'medium')")
    args = parser.parse_args()
    
    # Set the output path
    if args.output_path is None:
        output_path = args.input_path
    else:
        output_path = args.output_path

    input_path = args.input_path
    input_path = str(input_path)
    output_path = str(output_path)

    #  Transcribe the audio file and align the transcript
    word_segments = transcribe_and_align(input_path, args.device, args.model_type)
    word_segments = word_segments['word_segments']
    
    # Add the subtitles to the video
    add_subtitles_to_video(input_path, output_path, word_segments)

if __name__ == "__main__":
    main()




