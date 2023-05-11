import os
import requests
from typing import List, Dict, Optional

from PIL import Image, ImageDraw, ImageFont
from rembg import remove


def create_thumbnail(segmented_image:str,text:List[Dict],output_image="thumbnail.png"):
    # load the background image
    background_dimensions = (1280, 720)
    background = Image.new("RGB", background_dimensions, (0, 0, 0))

    # load the image to be placed on the right
    image = Image.open(segmented_image)
    
    # resize the image to fit on the background
    max_width = 6000
    max_height = background.height

    width, height = image.size
    if width > max_width or height > max_height:
        ratio = min(max_width/width, max_height/height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        image = image.resize((new_width, new_height))


    padding = 0 

    image_y = background.height - image.height - padding
    x_edge = background.width - image.width

    # place the image on the right side of the background
    background.paste(image, (x_edge, image_y))

    # create a draw object
    draw = ImageDraw.Draw(background)

    # iterate over the list of text objects and draw them on the left side of the background
    for item in text:
        # get the text and formatting information
        text = item["text"]
        color = item["color"]
        spacingTop = item["spacingTop"]
        size = item["size"]
        font_location = item['font']

        # set the font and color
        draw.text((30, spacingTop), text, font=ImageFont.truetype(font_location, size), fill=color,)

    # save the resulting image
    background.save(output_image)

def create_thumbnail(segmented_image: str, 
                     text_items: List[Dict[str, object]], 
                     output_image: Optional[str] = None, 
                     text_x_pos: int = 0, 
                     default_font_location: str = "arial.ttf",
                     y_spacing: int = 1) -> Image.Image:
    """
    Create a thumbnail image from a background, segmented image, and text.

    This function generates a thumbnail image by combining a provided segmented image with text
    drawn on the left side. The text_items parameter is a list of dictionaries, each containing
    the text to be drawn and its formatting options. The resulting image can be saved to disk
    or returned as a PIL.Image object.

    Args:
        segmented_image (str): Path to the segmented image file.
        text_items (List[Dict[str, object]]): A list of dictionaries containing the text and
            its formatting options. Each dictionary should have the following keys:
            - "text": The text string to be drawn.
            - "color": The text color in RGB format.
            - "size": The font size.
            - "font" (optional): Path to the font file. Defaults to arial.ttf.
            - "y_spacing" (optional): Vertical spacing between text lines. Defaults to 1.
        output_image (Optional[str], optional): Path to save the output image. If not provided,
            the function will return the generated image as a PIL.Image object.
        text_x_pos (int, optional): The x-coordinate of the starting position for the text.
            Defaults to 0.
        default_font_location (str, optional): Path to the default font file. Defaults to "arial.ttf".
        y_spacing (int, optional): Default vertical spacing between text lines. Defaults to 1.

    Returns:
        Image.Image: The generated thumbnail image. Returned only if output_image is not provided.
    """

    # Load the background image
    background_dimensions = (1280, 720)
    background_color = (0, 0, 0)
    background = Image.new("RGB", background_dimensions, background_color)

    # Load the image to be placed on the right
    image = Image.open(segmented_image)

    # Resize the image to fit on the background
    max_width = 6000  # This value seems too high for a thumbnail
    max_height = background.height

    width, height = image.size
    if width > max_width or height > max_height:
        ratio = min(max_width/width, max_height/height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        image = image.resize((new_width, new_height))

    # Calculate the y-coordinate of the image
    image_y = background.height - image.height

    # Place the image on the right side of the background
    background.paste(image, (background.width - image.width, image_y))

    # Create a draw object
    draw = ImageDraw.Draw(background)

    # Set default text position
    text_y_pos = 0

    # Iterate over the list of text objects and draw them on the left side of the background
    for item in text:
        # Get the text and formatting information
        text = item["text"]
        color = item["color"]
        y_spacing = item.get("y_spacing", y_spacing)
        size = item["size"]
        font_location = item.get("font", default_font_location)

        # Set the font and color
        font = ImageFont.truetype(font_location, size)
        text_width, text_height = draw.textsize(text, font=font)
        draw.text((text_x_pos, text_y_pos + y_spacing), text, font=font, fill=color)

        # Update the text position
        text_y_pos += text_height + y_spacing

    # Save the resulting image
    if output_image:
        background.save(output_image)
    else:
        return background

def segment_image(input_path:str,output_path:str):
    input = Image.open(input_path)
    output = remove(input)
    output.save(output_path)


def crop_png(input_data: str, output_data: str) -> None:
    """
    Crop a PNG image to the non-transparent area and save it to a file.

    Args:
        input_data (str): The path to the input image file.
        output_data (str): The path to save the cropped image file.

    Returns:
        None
    """
    # Open the image
    image = Image.open(input_data)

    # Get the size of the image
    width, height = image.size

    # Get the alpha channel of the image
    alpha = image.split()[-1]

    # Find the bounding box of the non-transparent part of the image
    bbox = alpha.getbbox()

    # Crop the image to the bounding box
    cropped_image = image.crop(bbox)

    # Save the cropped image
    cropped_image.save(output_data)


def crop_transparent(image_path: str, output_path: str):
    """Crop a transparent image and save to a file.

    Args:
        image_path (str): The path to the input image.
        output_path (str): The path to save the cropped image.

    Returns:
        None
    """
    # Open the image
    image = Image.open(image_path)

    # Get the size of the image
    width, height = image.size

    # Find the dimensions of the non-transparent part of the image
    left, top, right, bottom = width, height, 0, 0
    for x in range(width):
        for y in range(height):
            alpha = image.getpixel((x,y))[3]
            if alpha != 0:
                left = min(left, x)
                top = min(top, y)
                right = max(right, x)
                bottom = max(bottom, y)

    # Crop the image to the non-transparent part
    image = image.crop((left, top, right, bottom))

    # Save the cropped image
    image.save(output_path)



def download_image(url: str, directory: str = ".") -> str:
    """
    Download an image from a URL and save it to a directory.

    Args:
        url (str): The URL of the image to download.
        directory (str): The directory to save the image in. Defaults to the current directory.

    Returns:
        str: The file path of the downloaded image if successful, else None.
    """
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.basename(url)
        filepath = os.path.join(directory, filename)
        with open(filepath, "wb") as f:
            f.write(response.content)
        return filepath
    else:
        return None

    
def convert_to_png(sample:str) -> str:
    """
    Converts the input image file to PNG format if it is a JPEG file.

    Args:
        sample (str): The path to the input image file.

    Returns:
        str: The path to the output image file. If the input image file is already in PNG format, returns the original file path.
    """
    img = Image.open(sample)
    if img.format == "JPEG":
        img = img.convert("RGBA")
        os.remove(sample)
        # get the base file name and old extension
        base_name, old_extension = os.path.splitext(sample)

        # replace the old extension with ".png"
        new_file_path = base_name + ".png"
        img.save(new_file_path)
    else:
        new_file_path = sample
    return new_file_path


if __name__ == '__main__':

    data = "https://th.bing.com/th/id/R.3d79e075f692870894fc41d6304eb4f2?rik=GfJgXZ5%2b5MJCVQ&riu=http%3a%2f%2fwww.pixelstalk.net%2fwp-content%2fuploads%2f2016%2f05%2fReally-Cool-Image.jpg"
    data = "https://www.lockheedmartin.com/content/dam/lockheed-martin/eo/photo/news/features/2021/ai/ai-small-1920.jpg.pc-adaptive.768.medium.jpeg"
    data = "https://images.girlslife.com/posts/009/9250/shutterstock_406983616.jpg"
    data = "https://www.aaa.com/AAA/common/AAR/images/deice1.png"

        
    sample = download_image(data)
    ff = convert_to_png(sample)
    # segment_image(ff,ff)
    # crop_png(ff,ff)



    # default_font_location = r"C:\Users\isaya\Downloads\Press_Start_2P\PressStart2P-Regular.ttf"
    # default_font_location = "arial.ttf"
    # text = [
    #     {"text": "r/Petty revenge", "color" : (255,255,255), "spacingTop": 0, "size" : 90, "font": default_font_location},
    #     {"text": "", "color" : (255,0,0), "spacingTop": 90, "size" : 90, "font": default_font_location},
    #     {"text": "taken? I'll go to ", "color" : (255,255,255), "spacingTop": 180, "size" : 90, "font": default_font_location},
    #     {"text": "first class", "color" : (255, 215, 0), "spacingTop": 270, "size" : 90, "font": default_font_location}
    # ]

    # input_data = r"c:\Users\isaya\code_examples\Machine_Learning\img_manipulation\japanese_robot.jpg"
    # output_data = r"c:\Users\isaya\code_examples\Machine_Learning\img_manipulation\_robot.png"
    # segment_image(input_data,output_data)
    # crop_png(output_data,output_data)

    # default_font_location = "arial.ttf"
    # ff = r"c:\Users\isaya\code_examples\Machine_Learning\img_manipulation\toy_boat_0.jpg"
    # text = [
    #     {"text": "r/Petty revenge", "color" : (255,255,255), "size" : 90, "font": default_font_location},
    #     {"text": "Allow my seat to be", "color" : (255,0,0), "size" : 90, "font": default_font_location},
    #     {"text": "taken? I'll go to ", "color" : (255,255,255), "size" : 90, "font": default_font_location},
    #     {"text": "first class", "color" : (255,255,255), "size" : 90, "font": default_font_location},
    # ]
    # create_thumbnail(ff, text, "thumbnail.png",text_x_pos=20)


    # create_thumbnail(ff,text,"fuck.png")
    # create_thumbnail(output_data,text,"fuck.png")