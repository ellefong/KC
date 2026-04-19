# Source - https://stackoverflow.com/a/23489503
# Posted by Andres Kull, modified by community. See post 'Timeline' for change history
# Retrieved 2026-04-19, License - CC BY-SA 3.0

from PIL import Image
import io
from io import BytesIO
import discord
import requests

# This is for the images to run when requested

def send_pil_image(pil_img):
    # 1. Create a binary stream (buffer)
    with io.BytesIO() as image_binary:
        # 2. Save the PIL image into the buffer
        pil_img.save(image_binary, 'PNG')
        
        # 3. Seek to the start of the stream
        image_binary.seek(0)
        
        # 4. Create the discord.File object and send it
        discord_file = discord.File(fp=image_binary, filename='image.png')
        return discord_file

class CallImage():
    def __init__(self, image):
        self.image = image

def return_image():
    response = requests.get("https://www.image2url.com/r2/default/images/1776593920673-8df6a62e-8ae0-43c2-954d-bf8149474fe1.png")
    img = Image.open(BytesIO(response.content))
    return send_pil_image(img)