import sys
import os

# Append the parent directory of 'src' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.metadata import get_youtube_video_tags  # update this line
# from src.metadata

youtube_url = "https://www.youtube.com/watch?v=Af3ZG47oT7I"

x = get_youtube_video_tags.get_video_tags(youtube_url)
f=0

