# Source - https://stackoverflow.com/a/23489503
# Posted by Andres Kull, modified by community. See post 'Timeline' for change history
# Retrieved 2026-04-19, License - CC BY-SA 3.0

from PIL import Image
import io
from io import BytesIO
import discord
import requests

# This is for the images to run when requested

# Note this is the function for PNGs
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

def send_pil_image_gif(pil_img):
    # 1. Create a binary stream (buffer)
    with io.BytesIO() as image_binary:
        # 2. Save the PIL image into the buffer
        pil_img.save(image_binary, 'GIF', save_all=True, loop=0, duration=pil_img.info.get('duration', 100))
        
        # 3. Seek to the start of the stream
        image_binary.seek(0)
        
        # 4. Create the discord.File object and send it
        # discord_file = discord.File(fp=image_binary, filename='image.gif')
        file = discord.File(fp=image_binary, filename='animation.gif')
        return file

# Note this is the function class wrapper
class CallImage():
    def __init__(self, image):
        self.image = image

def return_image():
    response = requests.get("https://www.image2url.com/r2/default/images/1776593920673-8df6a62e-8ae0-43c2-954d-bf8149474fe1.png")
    img = Image.open(BytesIO(response.content))
    return send_pil_image(img)

def return_gif():
    response = requests.get("https://plain-wnam-prod-public.komododecks.com/202604/19/WtpbKFYW7VYmI5IZOV9A/image.png")
    img = Image.open(BytesIO(response.content))
    return send_pil_image_gif(img)

