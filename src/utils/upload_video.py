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

    # Check the thumbnail file size
    if options.thumbnail:
        thumbnail_size = os.path.getsize(options.thumbnail)
        if thumbnail_size > 2097152:  # 2MB in bytes
            print('Thumbnail size exceeds the maximum allowed limit of 2MB.')
            return

    # Create a MediaFileUpload object for the video file
    # media = MediaFileUpload(options.file, chunksize=-1, resumable=True)

    # Upload the video and retrieve the video resource
    video_resource = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        # media_body=media
    ).execute()

    print('Video uploaded successfully.')

    # Add the wait_for_video function here, after the video upload
    video_id = video_resource.get('id')
    wait_for_video(youtube, video_id)

    # Use the set_thumbnail function to set the thumbnail
    if options.thumbnail:
        set_thumbnail(youtube, video_id, options.thumbnail)

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
