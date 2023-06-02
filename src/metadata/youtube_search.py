import os
import urllib.request
import re
import requests
from dotenv import load_dotenv

def get_unique_video_ids(search_query):
    # Replace white spaces with a "+" symbol
    search_query = search_query.replace(" ", "+")
    
    # Create a URL to search on YouTube using the search query
    url = f"https://www.youtube.com/results?search_query={search_query}&sp=CAMSBAgEEAE%253D"
    
    # Open the URL and read the HTML response
    with urllib.request.urlopen(url) as html:
        html_content = html.read().decode()
    
    # Find all video IDs in the HTML content using a regular expression
    video_ids = re.findall(r"watch\?v=(\S{11})", html_content)
    
    # Convert the list of video IDs to a set to remove duplicates and then convert it back to a list
    unique_video_ids = list(set(video_ids))
    return unique_video_ids

def get_video_views(video_id, api_key):
    # Construct the API URL
    url = f'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={api_key}'

    # Make a GET request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Load the JSON response into a Python dictionary
        data = response.json()
    
        # Get the view count from the statistics object
        view_count = data['items'][0]['statistics']['viewCount']
    
        # Return the view count
        return view_count
    else:
        # If the request was not successful, raise an exception
        raise Exception(f'Error retrieving video data: {response.text}')

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Get the API key from the environment variable GOOGLE_API_KEY
    API_KEY = os.getenv('GOOGLE_API_KEY')

    # Check if the API key was successfully loaded
    if not API_KEY:
        raise Exception('Missing API key. Please set the environment variable GOOGLE_API_KEY in the .env file.')

    # Example usage
    search_query = "Mozart"
    video_ids = get_unique_video_ids(search_query)
    for video_id in video_ids:
        view_count = get_video_views(video_id, API_KEY)
        print(f'The video with ID {video_id} has {view_count} views.')

# Run the main function
if __name__ == "__main__":
    main()
