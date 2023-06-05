from metadata.get_youtube_video_tags import get_video_tags
from metadata.video_engagement_metrics import get_video_engagement_metrics

def collect_data(video_id, api_key):
    # Collect metadata about the video
    tags = get_video_tags(video_id, api_key)
    engagement_metrics = get_video_engagement_metrics(video_id, api_key)
    
    # Combine the tags and engagement metrics into one dictionary
    data = {**tags, **engagement_metrics}
    
    return data
