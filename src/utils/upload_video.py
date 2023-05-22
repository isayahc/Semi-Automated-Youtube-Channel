from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from argparse import Namespace
import argparse
import os

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_authenticated_service() -> build:
    """
    Handle OAuth2 authentication.
    Returns an authenticated service that can be used to interact with the YouTube API.
    """
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def initialize_upload(youtube: build, options: Namespace) -> None:
    """
    Initialize the video upload.
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
            privacyStatus=options.privacyStatus
        )
    )

    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True)
    )

    resumable_upload(youtube, insert_request, options)  # Add 'youtube' as a parameter



def resumable_upload(youtube: build, insert_request: object, options: Namespace) -> None:
    """
    Upload a file and track its progress.
    """
    response = None
    while response is None:
        status, response = insert_request.next_chunk()
        if 'id' in response:
            print(f"Video id {response['id']} was successfully uploaded.")
            set_thumbnail(youtube, options, response['id'])



def set_thumbnail(youtube: build, options: Namespace, video_id: str) -> None:
    """
    Set the thumbnail of the video after it has been uploaded.
    """
    youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(options.thumbnail)
    ).execute()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True, help='Video file to upload')
    parser.add_argument('--title', help='Video title', default='Test Title')
    parser.add_argument('--description', help='Video description', default='Test Description')
    parser.add_argument('--category', default='27', help='Numeric video category. See https://developers.google.com/youtube/v3/docs/videoCategories/list')
    parser.add_argument('--keywords', help='Video keywords, comma separated', default='')
    parser.add_argument('--privacyStatus', choices=['public', 'private', 'unlisted'], default='public', help='Video privacy status.')
    parser.add_argument('--thumbnail', help='Thumbnail image file', default='')
    args = parser.parse_args()

    youtube = get_authenticated_service()
    try:
        initialize_upload(youtube, args)
    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred:\n{e.content}')


if __name__ == '__main__':
    main()
