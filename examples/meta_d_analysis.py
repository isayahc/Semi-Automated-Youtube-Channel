import sys
import os

# Append the parent directory of 'src' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.metadata import get_youtube_video_tags, get_transcripts



sample = r".\not_for_github\Af3ZG47oT7I_en.srt"
# sample = r"C:\Users\isaya\code_projects\Machine_Learning\Semi-Automated-Youtube-Channel\not_for_github\Af3ZG47oT7I_en.srt"

# youtube_url = "https://www.youtube.com/watch?v=Af3ZG47oT7I"


jj = get_transcripts.srt_to_dict(sample)
# x = get_youtube_video_tags.get_video_tags(youtube_url)

f=0

