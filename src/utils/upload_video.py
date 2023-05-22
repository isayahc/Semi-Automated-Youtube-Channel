from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import argparse
import os

# This file contains the OAuth 2.0 information for this application, 
# including its client_id and client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"
# Define the scopes required by the API
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

# This function handles OAuth2 authentication.
# It returns an authenticated service that can be used to interact with the YouTube API.
def get_authenticated_service():
    # Create a flow object. This object holds the client_id and client_secret, 
    # and is used for OAuth2 authentication.
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    # Authenticate and construct the service.
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

# This function initializes the video upload.
def initialize_upload(youtube, options):
    # Process the command line arguments.
    tags = None
    if options.keywords:
        tags = options.keywords.split(',')

    # Construct the body of the request.
    body=dict(
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

    # Call the YouTube API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True)
    )

    # Execute the upload.
    resumable_upload(insert_request, options)

# This function uploads a file and tracks its progress.
def resumable_upload(request, options):
    response = None
    while response is None:
        status, response = request.next_chunk()
        # If the upload is successful, set the video's thumbnail.
        if 'id' in response:
            print(f"Video id {response['id']} was successfully uploaded.")
            set_thumbnail(options, response['id'])

# This function sets the thumbnail of the video after it has been uploaded.
def set_thumbnail(options, video_id):
    youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(options.thumbnail)
    ).execute()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Add arguments for command line options.
    parser.add_argument('--file', required=True, help='Video file to upload')
    parser.add_argument('--title', help='Video title', default='Test Title')
    parser.add_argument('--description', help='Video description', default='Test Description')
    parser.add_argument('--category', default='27', help='Numeric video category. ' + 'See https://developers.google.com/youtube/v3/docs/videoCategories/list')
    parser.add_argument('--keywords', help='Video keywords, comma separated', default='')
    parser.add_argument('--privacyStatus', choices=['public', 'private', 'unlisted'], default='public', help='Video privacy status.')
    parser.add_argument('--thumbnail', help='Thumbnail image file', default='')
    args = parser.parse_args()

    # Authenticate and initialize the service.
    youtube = get_authenticated_service()
    try:
        initialize_upload(youtube, args)
    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred:\n{e.content}')
