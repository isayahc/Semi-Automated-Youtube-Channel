import sys
import os

# Append the parent directory of 'src' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.metadata import get_youtube_video_tags  # update this line


sample = r"c:\Users\isaya\code_projects\Machine_Learning\Semi-Automated-Youtube-Channel\not_for_github\Af3ZG47oT7I_en.srt"

youtube_url = "https://www.youtube.com/watch?v=Af3ZG47oT7I"

# x = get_youtube_video_tags.get_video_tags(youtube_url)

load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv("GOOGLE_API_KEY")

f=0

