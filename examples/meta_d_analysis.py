import sys
import os
from dotenv import load_dotenv

# Append the parent directory of 'src' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.metadata import get_youtube_video_tags, get_transcripts
from src.metadata import video_engagement_metrics


sample = r".\not_for_github\Af3ZG47oT7I_en.srt"


# youtube_url = "https://www.youtube.com/watch?v=Af3ZG47oT7I"
vid_id = "Af3ZG47oT7I"
vid_id  = "rn8oef21Igg"

jj = get_transcripts.srt_to_dict(sample)
# x = get_youtube_video_tags.get_video_tags(youtube_url)

load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv("GOOGLE_API_KEY")

kk = video_engagement_metrics.YouTubeMetrics(api_key=api_key)

# mm = kk.get_video_engagement_metrics(vid_id)
mm = kk.get_video_comments(vid_id,50)

f=0

