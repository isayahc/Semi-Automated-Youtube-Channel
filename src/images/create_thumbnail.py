from typing import List, Dict, Optional
from PIL import Image, ImageDraw, ImageFont
import os

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


if __name__ == '__main__':
    default_font_location = "arial.ttf"
    ff = r"c:\Users\isaya\code_examples\Machine_Learning\img_manipulation\toy_boat_0.jpg"
    text = [
        {"text": "r/Petty revenge", "color" : (255,255,255), "size" : 90, "font": default_font_location},
        {"text": "Allow my seat to be", "color" : (255,0,0), "size" : 90, "font": default_font_location},
        {"text": "taken? I'll go to ", "color" : (255,255,255), "size" : 90, "font": default_font_location},
        {"text": "first class", "color" : (255,255,255), "size" : 90, "font": default_font_location},
    ]
    create_thumbnail(ff, text, "thumbnail.png",text_x_pos=20)
    x=0
