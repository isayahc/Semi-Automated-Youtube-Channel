from typing import List, Dict, Union, Tuple
from moviepy.editor import VideoFileClip

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