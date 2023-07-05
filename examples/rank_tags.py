import sys
import os
import pytrends
# Append the parent directory of 'src' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.metadata import get_youtube_video_tags  # update this line
from src.metadata import keyword_analysis


youtube_url = "https://www.youtube.com/watch?v=Af3ZG47oT7I"
youtube_url = "https://www.youtube.com/watch?v=m1sgtzgrhwY"
youtube_url = "https://www.youtube.com/watch?v=rn8oef21Igg"
youtube_url = "https://www.youtube.com/watch?v=G88XPaeGYFo"




tag_list = get_youtube_video_tags.get_video_tags(youtube_url)


pytrend_obj = keyword_analysis.generate_payload(tag_list)

sample = pytrend_obj.related_queries()

# pytrend_obj.
data = keyword_analysis.get_trends(tag_list)


keyword_analysis.plot_trends(data)

pytrends = pytrends.TrendReq(hl='en-US', tz=360)

x=0
