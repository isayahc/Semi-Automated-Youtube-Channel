import argparse
from moviepy.editor import VideoFileClip, concatenate_videoclips


def concatenate_videos(videos, output):
    # list of video clips
    video_clips = []

    for path in videos:
        # load video
        clip = VideoFileClip(path)
        clip = clip.subclip()

        # append clip to the list
        video_clips.append(clip)

    # concatenate the clips
    final_clip = concatenate_videoclips(video_clips)

    # write the final clip to file
    final_clip.write_videofile(output)


def main():
    # create a parser object
    parser = argparse.ArgumentParser(description="Concatenate a list of videos")

    # add an argument for the list of videos
    parser.add_argument("videos", nargs="+", type=str, help="the videos to concatenate")

    # add an argument for the output file name
    parser.add_argument("-o", "--output", type=str, default="final_video.mp4", help="the output file name")

    # parse the arguments
    args = parser.parse_args()

    # call the concatenate_videos function with the parsed arguments
    concatenate_videos(args.videos, args.output)


if __name__ == "__main__":
    main()
