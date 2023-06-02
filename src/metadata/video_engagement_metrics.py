import os
import argparse
from googleapiclient.discovery import build
from dotenv import load_dotenv

def get_video_engagement_metrics(video_id: str, api_key: str):
    """
    Fetch engagement metrics for a specific YouTube video.

    Args:
        video_id (str): The ID of the YouTube video.
        api_key (str): The Google API key.

    Returns:
        dict: A dictionary containing engagement metrics.
    """
    # Build the YouTube API client
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Make the API request to get video statistics
    response = youtube.videos().list(
        part='statistics',
        id=video_id
    ).execute()

    # Extract engagement metrics from the response
    engagement_metrics = response['items'][0]['statistics']

    return engagement_metrics

def get_video_comments(video_id: str, api_key: str, max_results: int = 20, include_replies: bool = True, order: str = 'relevance') -> list:
    """
    Fetch comments for a specific YouTube video.

    Args:
        video_id (str): The ID of the YouTube video.
        api_key (str): The Google API key.
        max_results (int, optional): Maximum number of comments to return. Defaults to 20.
        include_replies (bool, optional): If True, includes replies to comments. Defaults to True.
        order (str, optional): The order in which to retrieve comments.
            Possible values: 'relevance', 'time', 'rating', 'videoLikes', 'videoRelevance'.
            Defaults to 'relevance'.

    Returns:
        list: A list containing comments, booleans indicating if it is a reply, and the comment's publish datetime.
    """
    # Build the YouTube API client
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Fetch comments for the video with the specified order
    response = youtube.commentThreads().list(
        part='snippet,replies',
        videoId=video_id,
        textFormat='plainText',
        maxResults=max_results,
        order=order
    ).execute()

    # Extract comments from the response
    comments = []
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        comments.append((comment['textDisplay'], False, comment['publishedAt']))  # It's not a reply
        if include_replies and 'replies' in item:
            for reply in item['replies']['comments']:
                comments.append((reply['snippet']['textDisplay'], True, reply['snippet']['publishedAt']))  # It's a reply
        
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
