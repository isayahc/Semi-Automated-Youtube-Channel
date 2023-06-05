import os
import argparse
from googleapiclient.discovery import build
from dotenv import load_dotenv

def get_video_engagement_metrics(video_id: str, api_key: str) -> dict:
    """
    Fetch engagement metrics for a specific YouTube video.

    Args:
        video_id (str): The ID of the YouTube video.
        api_key (str): The Google API key.

    Returns:
        dict: A dictionary containing engagement metrics and video metadata.
    """
    # Build the YouTube API client
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Make the API request to get video statistics and snippet (for metadata)
    response = youtube.videos().list(
        part='statistics,snippet',
        id=video_id
    ).execute()

    # Extract engagement metrics and metadata from the response
    engagement_metrics = response['items'][0]['statistics']
    metadata = response['items'][0]['snippet']

    # Add metadata to the engagement metrics dictionary
    engagement_metrics.update(metadata)

    return engagement_metrics


def get_video_comments(video_id: str, api_key: str, max_results: int = 20, include_replies: bool = True) -> list:
    """
    Fetch comments for a specific YouTube video.

    Args:
        video_id (str): The ID of the YouTube video.
        api_key (str): The Google API key.
        max_results (int, optional): Maximum number of comments to return. Defaults to 20.
        include_replies (bool, optional): If True, includes replies to comments. Defaults to True.

    Returns:
        list: A list containing comments, booleans indicating if it is a reply, the comment's publish datetime, 
              like count, and author channel Id.
    """
    # Build the YouTube API client
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Fetch comments for the video
    response = youtube.commentThreads().list(
        part='snippet,replies',
        videoId=video_id,
        textFormat='plainText',
        maxResults=max_results
    ).execute()

    # Extract comments from the response
    comments = []
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        comments.append(
            {
                'text': comment['textDisplay'],
                'is_reply': False,
                'like_count': comment['likeCount'],
                'author_channel_id': comment['authorChannelId']['value'],
                'publish_time': comment['publishedAt']
            }
        )

        # Extract replies if any
        if include_replies and 'replies' in item:
            for reply in item['replies']['comments']:
                reply_comment = reply['snippet']
                comments.append(
                    {
                        'text': reply_comment['textDisplay'],
                        'is_reply': True,
                        'like_count': reply_comment['likeCount'],
                        'author_channel_id': reply_comment['authorChannelId']['value'],
                        'publish_time': reply_comment['publishedAt']
                    }
                )

    return comments


def main():
    # Load environment variables
    load_dotenv()

    # Get the API key from the environment variables
    api_key = os.getenv("GOOGLE_API_KEY")

    # Setup argument parser
    parser = argparse.ArgumentParser(description='Fetch engagement metrics or comments for a YouTube video.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--metrics', action='store_true', help='Get engagement metrics')
    group.add_argument('--comments', type=int, nargs='?', const=20, help='Get comments')
    parser.add_argument('--no-replies', action='store_true', help='Exclude replies to comments')
    parser.add_argument('--order', type=str, choices=['relevance', 'time', 'rating', 'videoLikes', 'videoRelevance'], default='relevance', help='Order of comments')
    parser.add_argument('video_id', type=str, help='The ID of the YouTube video')

    # Parse command-line arguments
    args = parser.parse_args()

    if args.metrics:
        # Get and print engagement metrics
        engagement_metrics = get_video_engagement_metrics(args.video_id, api_key)
        print(engagement_metrics)
    elif args.comments is not None:
        # Get and print comments
        comments = get_video_comments(args.video_id, api_key, args.comments, not args.no_replies, args.order)
        for comment, is_reply, datetime in comments:
            print(f'{"Reply" if is_reply else "Comment"} ({datetime}): {comment}')

if __name__ == "__main__":
    main()
