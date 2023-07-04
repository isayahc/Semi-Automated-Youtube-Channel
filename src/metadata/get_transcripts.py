import argparse
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter
import os

def main():
    parser = argparse.ArgumentParser(description='Check if the transcript of a YouTube video is auto-generated or user-generated')
    parser.add_argument('video_id', type=str, help='the ID of the YouTube video')
    parser.add_argument('--save', type=str, help='save the transcript as an SRT file if it is user-generated')
    args = parser.parse_args()

    transcript_list = YouTubeTranscriptApi.list_transcripts(args.video_id)

    for transcript in transcript_list:
        if not transcript.is_generated:
            print("User-generated transcript")
            if args.save:
                if os.path.isdir(args.save):
                    srt = SRTFormatter().format_transcript(transcript.fetch())
                    with open(os.path.join(args.save, f"{args.video_id}.srt"), "w") as f:
                        f.write(srt)
                else:
                    srt = SRTFormatter().format_transcript(transcript.fetch())
                    with open(args.save, "w") as f:
                        f.write(srt)
        else:
            print("Auto-generated transcript")

if __name__ == '__main__':
    main()
