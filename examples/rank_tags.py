import sys
import os

# Append the parent directory of 'src' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.metadata import get_youtube_video_tags  # update this line
from src.metadata import keyword_analysis


youtube_url = "https://www.youtube.com/watch?v=Af3ZG47oT7I"
youtube_url = "https://www.youtube.com/watch?v=m1sgtzgrhwY"
youtube_url = "https://www.youtube.com/watch?v=rn8oef21Igg"

tag_list = get_youtube_video_tags.get_video_tags(youtube_url)
data = keyword_analysis.get_trends(tag_list)
keyword_analysis.plot_trends(data)
x=0
