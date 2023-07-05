import sys
import os
import pytrends
# Append the parent directory of 'src' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.metadata import get_youtube_video_tags  # update this line
from src.metadata import keyword_analysis

data = [
"https://www.youtube.com/watch?v=Af3ZG47oT7I",
"https://www.youtube.com/watch?v=m1sgtzgrhwY",
"https://www.youtube.com/watch?v=rn8oef21Igg",
"https://www.youtube.com/watch?v=G88XPaeGYFo",]

# tag_list = get_youtube_video_tags.get_video_tags(youtube_url)

dataa = [get_youtube_video_tags.get_video_tags(i) for i in data]

x=0