
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests


def save_image_from_url(url):
    # Fetch the image from the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Return the binary content of the image
        return response.content
    
    else:
        raise Exception("Failed to fetch image from URL")
    

def update_image(image_data, text_upper, text_lower):
  
    image = Image.open(BytesIO(save_image_from_url(image_data)))
    border = 50  # Thickness of the border/frame
    new_width = image.width + border * 2
    new_height = image.height + border * 2

    # Create a new image with the increased dimensions.
    # The frame color will fill this new image.
    frame_color = (255, 255, 255)  # Using white as the frame color for the example.
    new_image = Image.new("RGB", (new_width, new_height), frame_color)

    # Paste the original image onto the center of the new image.
    new_image.paste(image, (border, border))

    # Prepare to write text on the image.
    draw = ImageDraw.Draw(new_image)
    # Define the text properties.
    font = ImageFont.truetype("Chalkduster.ttf", 85)   # Adjust the font size as needed.
    # Calculate the position for the text to be centered on the border.
    text_x = 55
    text_y = 20
    # Choose a text color that contrasts the frame color.
    text_color = (0, 0, 255)  # Black color for the text.
    # Write the text onto the image.
    #draw transparent background rectangle
    draw.rectangle(((0, 0), (new_image.width, 150)), fill=(255, 255, 255, 128))
    draw.text((text_x, text_y), text_upper, fill=text_color, font=font)


    font = ImageFont.truetype("Chalkduster.ttf", 75)   # Adjust the font size as needed.
    # Calculate the position for the text to be centered on the border.
    text_x = image.width - image.width/2
    text_y = image.height - 25
    # Choose a text color that contrasts the frame color.
    text_color = (255, 0, 0)  # Black color for the text.
    # Write the text onto the image.
    ##draw transparent background rectangle
    draw.rectangle(((0, image.height-85), (new_image.width, new_image.height)), fill=(255, 255, 255, 128))
    draw.text((text_x, text_y), text_lower, fill=text_color, font=font)

    img_byte_arr = BytesIO()
    new_image.save(img_byte_arr, format='JPEG')  # Save the image as JPEG into the BytesIO object
    # Get the binary representation of the image
    img_binary = img_byte_arr.getvalue()

    return  img_binary