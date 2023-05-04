import argparse
import pathlib
import subprocess
from typing import Tuple
from PIL import Image

def create_webm_video(input_img: str, input_audio: str, output_file: str, output_extension: str = "mp4", img_size: Tuple[int, int] = (1080,1920)) -> None:
    # Resize the input image to a resolution of 1920x1080
    image = Image.open(input_img)
    resized_image = image.resize(img_size)
    resized_image.save(input_img)

    # Use the resized image and highest quality settings to create the video
    output_extension = "mp4"
    output_path = pathlib.Path(output_file)
    output_path = output_path.with_suffix(f".{output_extension}")
    # command = ['ffmpeg', '-loop', '1', '-i', input_img, '-i', input_audio, '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '0', '-c:a', 'libopus', '-strict -2', str(output_path), '-y']
    command = ['ffmpeg', '-loop', '1', '-i', input_img, '-i', input_audio, "-vcodec", "mpeg4", "-acodec", "aac", '-shortest', str(output_path) , "-y","-r","2"]
    print(command)
    subprocess.run(command)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a webm video using an input image and audio.")
    parser.add_argument("input_img", help="Path to the input image")
    parser.add_argument("input_audio", help="Path to the input audio")
    parser.add_argument("output_file", help="Name of the output video file")
    parser.add_argument("-e", "--output_extension", help="Extension of the output video file", default="webm")
    # parser.add_argument("-s", "--img_size", help="Resolution of the output video (WIDTHxHEIGHT)", default="1920x1080")

    args = parser.parse_args()
    # img_size = tuple(map(int, args.img_size.split("x")))
    create_webm_video(args.input_img, args.input_audio, args.output_file, args.output_extension, )#img_size)
