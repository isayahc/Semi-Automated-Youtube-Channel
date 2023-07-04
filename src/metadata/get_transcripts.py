import argparse
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter
import os
import pysrt
import chardet


def get_encoding_type(srt_file):
    rawdata = open(srt_file, 'rb').read()
    result = chardet.detect(rawdata)
    return result['encoding']

def srt_to_dict(srt_file):
    encoding = get_encoding_type(srt_file)
    subs = pysrt.open(srt_file, encoding=encoding)

    list_dict = []
    for sub in subs:
        list_dict.append({
            'start_seconds': sub.start.ordinal / 1000.0,
            'end_seconds': sub.end.ordinal / 1000.0,
            'text': sub.text
        })

    return list_dict

def main():
    parser = argparse.ArgumentParser(description='Check if the transcript of a YouTube video is auto-generated or user-generated')
    parser.add_argument('video_id', type=str, help='the ID of the YouTube video')
    parser.add_argument('--save', type=str, help='save the transcript as an SRT file if it is user-generated')
    parser.add_argument('--language_codes', type=str, nargs='*', default=["en"], help='the language codes of the desired transcripts')
    args = parser.parse_args()

    transcript_list = YouTubeTranscriptApi.list_transcripts(args.video_id)

    for language_code in args.language_codes:
        if language_code in transcript_list._manually_created_transcripts:
            transcript = transcript_list._manually_created_transcripts[language_code]
            print(f"User-generated transcript for language: {language_code}")
            if args.save:
                srt = SRTFormatter().format_transcript(transcript.fetch())
                if os.path.isdir(args.save):
                    with open(os.path.join(args.save, f"{args.video_id}_{language_code}.srt"), "w") as f:
                        f.write(srt)
                else:
                    with open(f"{args.save}_{language_code}.srt", "w") as f:
                        f.write(srt)
        else:
            print(f"Auto-generated transcript or no transcript available for language: {language_code}")

if __name__ == '__main__':
    main()
