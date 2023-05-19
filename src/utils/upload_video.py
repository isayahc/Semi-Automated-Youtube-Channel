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


def retry_on_exceptions(func, retries=MAX_RETRIES):
    """
    Retries a function in case of retriable exceptions.

    Args:
        func: The function to retry.
        retries: The number of retries to attempt. Defaults to MAX_RETRIES.
    """
    retry = 0
    while retry <= retries:
        try:
            return func()
        except RETRIABLE_EXCEPTIONS as e:
            print(f'Retriable error occurred: {e}')
            retry += 1
            sleep_seconds = random.random() * (2 ** retry)
            print(f'Sleeping {sleep_seconds} seconds and then retrying...')
            time.sleep(sleep_seconds)
    raise Exception('Maximum retry attempts exhausted')


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

    # Invoke the upload_chunk function
    return upload_chunk()


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
    args = parser.parse_args()

    youtube = get_authenticated_service()
    try:
        initialize_upload(youtube, args)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
