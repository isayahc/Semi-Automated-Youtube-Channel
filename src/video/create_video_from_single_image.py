import argparse
import pathlib
import subprocess
from typing import Tuple
from PIL import Image

def create_video_from_single_image(input_img: str, input_audio: str, output_file: str, output_extension: str = "mp4", img_size: Tuple[int, int] = (1080, 1920)) -> None:
    """
    Creates a video using an input image and audio, with the specified output extension and image size.
    
    :param input_img: Path to the input image file.
    :param input_audio: Path to the input audio file.
    :param output_file: Name of the output video file.
    :param output_extension: Extension of the output video file. Default is 'mp4'.
    :param img_size: Tuple containing the desired image width and height. Default is (1080, 1920).
    """
    # Resize the input image to the specified resolution
    image = Image.open(input_img)
    resized_image = image.resize(img_size)
    resized_image.save(input_img)

    # Create the video using the resized image and specified output extension
    output_path = pathlib.Path(output_file)
    output_path = output_path.with_suffix(f".{output_extension}")
    command = ['ffmpeg', '-loop', '1', '-i', input_img, '-i', input_audio, "-vcodec", "mpeg4", "-acodec", "aac", '-shortest', str(output_path), "-y", "-r", "2"]
    print(command)
    subprocess.run(command)


def main():
    parser = argparse.ArgumentParser(description="Create a video using an input image and audio.")
    parser.add_argument("input_img", help="Path to the input image")
    parser.add_argument("input_audio", help="Path to the input audio")
    parser.add_argument("output_file", help="Name of the output video file")
    parser.add_argument("-e", "--output_extension", help="Extension of the output video file", default="mp4")

    args = parser.parse_args()
    create_video_from_single_image(args.input_img, args.input_audio, args.output_file, args.output_extension)

if __name__ == "__main__":
    main()
