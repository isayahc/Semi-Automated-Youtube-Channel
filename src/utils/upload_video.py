from argparse import Namespace
import argparse
import os

from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from moviepy.editor import VideoFileClip


CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
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


def validate_shorts(options: Namespace) -> None:
    """
    Validate that the video file meets the requirements for YouTube Shorts.

    Parameters:
        options (Namespace): Command line arguments.
    """
    # Check the video format and duration
    video = VideoFileClip(options.file)
    width, height = video.size
    duration = video.duration

    # Check if video is vertical (aspect ratio of 9:16)
    if width / height != 9 / 16:
        raise ValueError("Video is not in the correct aspect ratio for YouTube Shorts. It must be a vertical video (aspect ratio 9:16).")

    # Check if video is no longer than 60 seconds
    if duration > 60:
        raise ValueError("Video is too long for YouTube Shorts. It must be 60 seconds or less.")


def initialize_upload(youtube: build, options: Namespace) -> None:
    """
    Initialize the video upload to YouTube.
    
    Parameters:
        youtube (build): The authenticated YouTube API service.
        options (Namespace): Command line arguments.
    """
    tags = None
    if options.keywords:
        tags = options.keywords.split(',')

    # Check if the video is a YouTube short and append "#Shorts" to the title
    title = options.title
    if options.youtubeShort:
        title += " #Shorts"

    body=dict(
        snippet=dict(
            title=title,
            description=options.description,
            tags=tags,
            categoryId=options.category
        ),
        status=dict(
            privacyStatus=options.privacyStatus,
            madeForKids=options.madeForKids  
        )
    )

    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True)
    )
    
    resumable_upload(youtube, insert_request, options)

def resumable_upload(youtube: build, insert_request: object, options: Namespace) -> None:
    """
    Upload the video file to YouTube and track its progress.
    
    Parameters:
        youtube (build): The authenticated YouTube API service.
        insert_request (object): The insert request object.
        options (Namespace): Command line arguments.
    """
    response = None
    while response is None:
        status, response = insert_request.next_chunk()
        if 'id' in response:
            print(f"Video id {response['id']} was successfully uploaded.")
            set_thumbnail(youtube, options, response['id'])

def set_thumbnail(youtube: build, options: Namespace, video_id: str) -> None:
    """
    Set the thumbnail of the uploaded video.
    
    Parameters:
        youtube (build): The authenticated YouTube API service.
        options (Namespace): Command line arguments.
        video_id (str): The ID of the uploaded video.
    """
    youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(options.thumbnail)
    ).execute()

def main():
    """
    Parse command line arguments and upload a video to YouTube.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True, help='Video file to upload')
    parser.add_argument('--title', help='Video title', default='Test Title')
    parser.add_argument('--description', help='Video description', default='Test Description')
    parser.add_argument('--category', default='27', help='Numeric video category. See https://developers.google.com/youtube/v3/docs/videoCategories/list')
    parser.add_argument('--keywords', help='Video keywords, comma separated', default='')
    parser.add_argument('--privacyStatus', choices=['public', 'private', 'unlisted'], default='private', help='Video privacy status.')
    parser.add_argument('--thumbnail', help='Thumbnail image file', default='')
    parser.add_argument('--madeForKids', type=bool, default=False, help='Made for kids field.')
    parser.add_argument('--youtubeShort', type=bool, default=False, help='Is this a YouTube short, if so it must have a aspect ratio of 9:16?')  # Added 'youtubeShort' argument
    args = parser.parse_args()

    if args.youtubeShort:
        validate_shorts(args)

    youtube = get_authenticated_service()
    try:
        initialize_upload(youtube, args)
    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred:\n{e.content}')

if __name__ == '__main__':
    main()