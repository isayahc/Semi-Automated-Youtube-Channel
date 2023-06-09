import random
import argparse

from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip



def create_clip_with_matching_audio(video_path: str, audio_path: str, output_path: str) -> None:
    """
    Create a video clip with the same duration as the provided audio file.
    The video clip is extracted from the input video file and the audio is set to the provided audio file.
    The resulting clip is saved to the output path.

    Args:
        video_path (str): The path to the input video file.
        audio_path (str): The path to the input audio file.
        output_path (str): The path to the output file where the resulting video clip will be saved.

    Returns:
        None
    """
    # Load video and audio files
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    # Set duration of clip to match audio file
    duration = audio.duration

    # Get a random start time for the clip
    start_time = random.uniform(0, video.duration - duration)

    # Extract clip from the video
    clip = video.subclip(start_time, start_time + duration)

    # Set the audio of the clip to the audio file
    clip = clip.set_audio(audio)

    # Save the clip
    clip.write_videofile(output_path, audio_codec="aac")


def main():
    parser = argparse.ArgumentParser(description='Create a video clip with matching audio')
    parser.add_argument('video_path', type=str, help='path to video file')
    parser.add_argument('audio_path', type=str, help='path to audio file')
    parser.add_argument('output_path', type=str, help='path to output file')
    args = parser.parse_args()
    create_clip_with_matching_audio(args.video_path, args.audio_path, args.output_path)


if __name__ == "__main__":
    main()
