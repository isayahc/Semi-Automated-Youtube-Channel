import os
import argparse
from googleapiclient.discovery import build
from dotenv import load_dotenv


class YouTubeMetrics:
    def __init__(self, api_key):
        self.youtube = build('youtube', 'v3', developerKey=api_key)

    def get_video_engagement_metrics(self, video_id):
        response = self.youtube.videos().list(
            part='statistics,snippet',
            id=video_id
        ).execute()

        engagement_metrics = response['items'][0]['statistics']
        metadata = response['items'][0]['snippet']

        engagement_metrics.update(metadata)

        return engagement_metrics

    def get_video_comments(self, video_id, max_results=20, include_replies=True):
        response = self.youtube.commentThreads().list(
            part='snippet,replies',
            videoId=video_id,
            textFormat='plainText',
            maxResults=max_results
        ).execute()

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
