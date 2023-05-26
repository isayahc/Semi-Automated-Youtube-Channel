from argparse import Namespace
import os
import datetime

from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl', 'https://www.googleapis.com/auth/youtube.readonly']

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service() -> build:
    """
    Authenticate the user using OAuth2.

    Returns:
        The authenticated service that can be used to interact with the YouTube API.
    """
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def get_comments(youtube, video_id, stop_date=None):
    """
    Fetch all comments of a video.
    
    Parameters:
        youtube (build): The authenticated YouTube API service.
        video_id (str): The ID of the YouTube video.
        stop_date (datetime): The date until comments should be fetched. Defaults to None, which fetches all comments.
        
    Returns:
        A list of all comments on the video until the specified date.
    """
    comments = []
    try:
        results = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=100  # maximum allowed per request
        ).execute()

        while results:
            for item in results["items"]:
                comment = item["snippet"]["topLevelComment"]
                comment_date = datetime.datetime.strptime(comment["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%S%z")
                if stop_date is None or comment_date <= stop_date:
                    comments.append(comment["snippet"]["textDisplay"])
                else:
                    return comments

            # check if there are more comments
            if "nextPageToken" in results:
                results = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    textFormat="plainText",
                    pageToken=results["nextPageToken"],
                    maxResults=100
                ).execute()
            else:
                break
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")

    return comments


def main():
    youtube = get_authenticated_service()
    video_id = "YOUR_VIDEO_ID"  # replace with your video ID
    stop_date = None  # replace with your date or leave as None to fetch all comments
    comments = get_comments(youtube, video_id, stop_date)
    for comment in comments:
        print(comment)


if __name__ == '__main__':
    main()
