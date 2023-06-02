import argparse
from YoutubeTags import videotags

def get_video_tags(video_url: str) -> list:
    """Get a list of tags for a YouTube video.

    Args:
        video_url (str): URL of the YouTube video.

    Returns:
        list: List of tags for the video, or an empty list if tags could not be retrieved.
    """
    try:
        findtags = videotags(video_url)
        return [tag.strip() for tag in findtags.split(",")]
    except Exception as e:
        print(f"An error occurred while retrieving tags for the video: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description='Get YouTube video tags')
    parser.add_argument('url', type=str, help='YouTube video URL')

    args = parser.parse_args()

    tags = get_video_tags(args.url)
    print(tags)

if __name__ == "__main__":
    main()
