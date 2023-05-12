import moviepy.editor as mp
import argparse
from pathlib import Path
import time


def split_video(input_path: Path, output_path: Path, start_time: int, end_time: int) -> None:
    """
    Split a video file into a specified section.

    Args:
        input_path (Path): The path to the input video file.
        output_path (Path): The path to the output video file.
        start_time (int): The starting time in seconds.
        end_time (int): The ending time in seconds.

    Raises:
        ValueError: If the input video file does not exist or if the start or end times are invalid.

    """
    if not input_path.exists():
        raise ValueError(f"Input file {input_path} does not exist.")

    if not isinstance(start_time, int) or not isinstance(end_time, int) or start_time < 0 or end_time < 0:
        raise ValueError("Start and end times must be non-negative integers.")

    video = mp.VideoFileClip(str(input_path))

    video_clip = video.subclip(start_time, end_time)

    try:
        video_clip.write_videofile(str(output_path), fps=24)
    except OSError:
        print("Error: Unable to write output file.")
        time.sleep(10)
        output_path.unlink()
        video_clip.write_videofile(str(output_path), fps=24)


def main():
    # Parse the command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", type=Path, help="The path to the input video file")
    parser.add_argument("output_path", type=Path, help="The path to the output video file")
    parser.add_argument("start_time", type=int, help="The starting time in seconds")
    parser.add_argument("end_time", type=int, help="The ending time in seconds")
    args = parser.parse_args()

    # Call the cut_video function with the parsed arguments
    input_path = args.input_path
    output_path = args.output_path
    start_time = args.start_time
    end_time = args.end_time
    split_video(input_path, output_path, start_time, end_time)

if __name__ == "__main__":
    main()