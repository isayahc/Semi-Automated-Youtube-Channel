#!/usr/bin/python

"""
This module provides a CLI tool to upload videos to YouTube using the YouTube Data API.

The tool accepts command line arguments for specifying details of the video to be uploaded including
the video file location, title, description, category, and keywords. It also handles retry logic for
failed uploads.

The tool uses OAuth 2.0 to authorize the upload request and allows resumable uploads for better
efficiency, especially when dealing with large video files.

To use this tool, you need to specify a client_secret.json file with your OAuth 2.0 client ID and
client secret. You can acquire these from the Google Cloud Console.
"""

import argparse
from http import client
import httplib2
import os
import random
import time
from dotenv import load_dotenv

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, client.NotConnected,
                        client.IncompleteRead, client.ImproperConnectionState,
                        client.CannotSendRequest, client.CannotSendHeader,
                        client.ResponseNotReady, client.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

VALID_PRIVACY_STATUSES = ('public', 'private', 'unlisted')

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

def get_my_uploaded_videos_details(youtube, max_results=25, part="snippet,contentDetails"):
    """
    Retrieves and returns the details of videos on the authenticated user's YouTube channel.

    Parameters:
    youtube: An authorized YouTube resource object.
    max_results: The maximum number of results to return (default 25).
    part: The part parameter specifies the video resource properties that the API response will include (default "snippet,contentDetails").

    Returns:
    A list of dictionaries containing details of each video.
    """
    try:
        # Get the channel data for the authenticated user
        channels_response = youtube.channels().list(mine=True, part='contentDetails').execute()
    except Exception as e:
        print(f"Failed to get channel data: {e}")
        return None

    cleaned_data = []
    
    # Get the ID of the 'uploads' playlist
    for channel in channels_response['items']:
        try:
            uploads_playlist_id = channel['contentDetails']['relatedPlaylists']['uploads']

            # Get the playlist items
            playlistitems_response = youtube.playlistItems().list(
                part=part,
                maxResults=max_results,
                playlistId=uploads_playlist_id
            ).execute()

            for item in playlistitems_response['items']:
                video_data = clean_video_data(item)
                cleaned_data.append(video_data)
                
        except Exception as e:
            print(f"Failed to get playlist items: {e}")

    return cleaned_data


def clean_video_data(item):
    """
    Cleans raw video data.

    Parameters:
    item: A dictionary containing raw video data.

    Returns:
    A dictionary containing cleaned video data.
    """
    video_data = {}
    video_data['video_id'] = item['contentDetails']['videoId']
    video_data['title'] = item['snippet']['title']
    video_data['description'] = item['snippet']['description']
    video_data['published_at'] = item['snippet']['publishedAt']
    video_data['thumbnails'] = item['snippet']['thumbnails']

    return video_data

def get_most_recent_video(youtube, max_results=25, part="snippet,contentDetails"):
    """
    Retrieves and returns the details of the most recently uploaded video on the authenticated user's YouTube channel.

    Parameters:
    youtube: An authorized YouTube resource object.
    max_results: The maximum number of results to return (default 25).
    part: The part parameter specifies the video resource properties that the API response will include (default "snippet,contentDetails").

    Returns:
    A dictionary containing details of the most recently uploaded video, or None if no videos were found.
    """
    cleaned_data = get_my_uploaded_videos_details(youtube, max_results, part)

    if not cleaned_data:
        print("No videos found.")
        return None

    # Sort the cleaned data by the 'published_at' key in descending order
    cleaned_data.sort(key=lambda x: x['published_at'], reverse=True)

    # Return the first item, which is the most recently uploaded video
    return cleaned_data[0]


def get_authenticated_service():
    """
    Authorize the request and store authorization credentials.
    """
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def set_thumbnail(youtube, video_id, thumbnail_path):
    """
    Set a thumbnail for a video.

    Args:
        youtube: An authorized youtube resource object.
        video_id: The ID of the video to set the thumbnail for.
        thumbnail_path: The path to the thumbnail image file.
    """
    media = MediaFileUpload(thumbnail_path, mimetype='image/jpeg')
    request = youtube.thumbnails().set(
        videoId=video_id,
        media_body=media
    )
    response = request.execute()

    print(f'Thumbnail set for video id "{video_id}".')

def initialize_upload(youtube, options):
    """
    Initialize the video upload process.
    """
    tags = None
    if options.keywords:
        tags = options.keywords.split(',')

    body = dict(
        snippet=dict(
            title=options.title,
            description=options.description,
            tags=tags,
            categoryId=options.category
        ),
        status=dict(
            privacyStatus=options.privacyStatus,
            selfDeclaredMadeForKids=False
        )
    )

    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True)
    )

    resumable_upload(insert_request)

    print('Video uploaded successfully.')

    # Use the set_thumbnail function to set the thumbnail
    if options.thumbnail:
        

        print("uploading image")
        # get_most_recent_video(youtube)
        most_recent_video = get_most_recent_video(youtube)

        # may be problematic but it assumes the most recently 
        # uploaded video is the video uploaded in this function
        most_recent_video_id = most_recent_video['video_id']
        set_thumbnail(youtube, most_recent_video_id , options.thumbnail)

    


def resumable_upload(request):
    """
    Performs a resumable upload of a file.

    Args:
        request: The media upload request to perform.
    """
    def upload_chunk():
        print('Uploading file...')
        status, response = request.next_chunk()
        if 'id' in response:
            print(f'Video id "{response["id"]}" was successfully uploaded.')
        else:
            print(f'The upload failed with an unexpected response: {response}')
            return None

        return response

def check_video_status(youtube, video_id):
    """
    Check the processing status of a video.

    Args:
        youtube: An authorized youtube resource object.
        video_id: The ID of the video to check.

    Returns:
        True if the video has finished processing, False otherwise.
    """
    request = youtube.videos().list(
        part="processingDetails",
        id=video_id
    )
    response = request.execute()

    status = response['items'][0]['processingDetails']['processingStatus']
    return status == "processed"

# Continuously check the status of the video
def wait_for_video(youtube, video_id):
    while True:
        if check_video_status(youtube, video_id):
            print("Video processing finished.")
            break
        else:
            print("Video still processing, waiting...")
            time.sleep(10)  # wait for 10 seconds before checking again


def get_most_recent_video(youtube, max_results=25, part="snippet,contentDetails"):
    """
    Retrieves and returns the details of the most recently uploaded video on the authenticated user's YouTube channel.

    Parameters:
    youtube: An authorized YouTube resource object.
    max_results: The maximum number of results to return (default 25).
    part: The part parameter specifies the video resource properties that the API response will include (default "snippet,contentDetails").

    Returns:
    A dictionary containing details of the most recently uploaded video, or None if no videos were found.
    """
    cleaned_data = get_my_uploaded_videos_details(youtube, max_results, part)

    if not cleaned_data:
        print("No videos found.")
        return None

    # Sort the cleaned data by the 'published_at' key in descending order
    cleaned_data.sort(key=lambda x: x['published_at'], reverse=True)

    # Return the first item, which is the most recently uploaded video
    return cleaned_data[0]


def validate_arguments(options):
    """
    Validate the command line arguments.
    """
    if options.thumbnail:
        thumbnail_size = os.path.getsize(options.thumbnail)
        if thumbnail_size > 2097152:  # 2MB in bytes
            print('Thumbnail size exceeds the maximum allowed limit of 2MB.')
            return False
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True, help='Video file to upload')
    parser.add_argument('--title', help='Video title', default='Test Title')
    parser.add_argument('--description', help='Video description',
                        default='Test Description')
    parser.add_argument('--category', default='27',
                        help='Numeric video category. ' +
                        'See https://developers.google.com/youtube/v3/docs/videoCategories/list')
    parser.add_argument('--keywords', help='Video keywords, comma separated',
                        default='')
    parser.add_argument('--privacyStatus', choices=VALID_PRIVACY_STATUSES,
                        default='private', help='Video privacy status.')
    parser.add_argument('--thumbnail', help='Path to thumbnail image file')
    args = parser.parse_args()

    if not validate_arguments(args):
        raise ValueError('Invalid arguments. Please check the provided values.')

    youtube = get_authenticated_service()
    try:
        initialize_upload(youtube, args)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
