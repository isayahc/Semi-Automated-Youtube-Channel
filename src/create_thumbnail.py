from typing import List, Dict, Optional
from PIL import Image, ImageDraw, ImageFont
import os

def create_thumbnail(segmented_image: str, 
                     text: List[Dict[str, object]], 
                     output_image: Optional[str] = None, 
                     text_x_pos: int = 0, 
                     default_font_location: str = "arial.ttf",
                     y_spacing: int = 1) -> Image.Image:
    # load the background image
    background_dimensions = (1280, 720)
    background_color = (0, 0, 0)
    background = Image.new("RGB", background_dimensions, background_color)

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

    # calculate the y-coordinate of the image
    image_y = background.height - image.height

    # place the image on the right side of the background
    background.paste(image, (background.width - image.width, image_y))

    # create a draw object
    draw = ImageDraw.Draw(background)

    # set default text position
    text_y_pos = 0

    # iterate over the list of text objects and draw them on the left side of the background
    for item in text:
        # get the text and formatting information
        text = item["text"]
        color = item["color"]
        y_spacing = item.get("y_spacing", y_spacing)
        size = item["size"]
        font_location = item['font'] if 'font' in item else default_font_location

        # set the font and color
        font = ImageFont.truetype(font_location, size)
        text_width, text_height = draw.textsize(text, font=font)
        draw.text((text_x_pos, text_y_pos + y_spacing), text, font=font, fill=color)

        # update the text position
        text_y_pos += text_height + y_spacing

    # save the resulting image
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
