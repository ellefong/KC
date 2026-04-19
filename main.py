import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from PIL import Image
import image

# This file is for the bot to run based on imput

#variables
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='dicord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

undercover = "Kracken" # this is for the Roles portion if we want it 

random_number = 0

# Array for banned words
# kick(3 types = ban) = ["shit", "fuck", "damn"]

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")

# This prints a warning message if you type curse words
@bot.event
async def on_message(message):

    if message.author == bot.user:
            return
    if "Kracken! Let's play a game!" in message.content.lower(): 
        await message.channel.send("Ok!!! Guess a number from 1 to 10")

    if "damn" in message.content.lower(): # Note add an array of curse words later
    # Past used words incase it doesnt work: shit, fuck, puto, PENDEJO, 
        await message.delete()
        await message.channel.send(f"{message.author.mention} DO NOT.")
    if "test image" in message.content.lower(): # author types test image
        await message.channel.send(file=image.return_image()) #or
        await message.channel.send(f"{message.author.mention} this is running.")
        # await ctx.message.channel.send(url='string')
        
    await bot.process_commands(message) #this is needed to be called

# This prints a Hello Message from the bot if you use an "!"
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=undercover)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} has been assigned to {undercover}")
    else:
        await ctx.send("This role doesn't exist")

# This removes a role
@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=undercover)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {undercover} role removed")
    else:
        await ctx.send("This role doesn't exist")

#TEST 
#try: getting bot to print photo
# Source - https://stackoverflow.com/a/67269535
# Posted by Jonas
# Retrieved 2026-04-19, License - CC BY-SA 4.0

@bot.command() 
async def readMessageURL(ctx):
    string = ctx.message.attachments[0]
    

    
##image stuff
# await ctx.message.channel.send(file=discord.File('path/to/image.png')) #or
# await ctx.message.channel.send(url='string')

try:
    bot.run(token, log_handler=handler, log_level=logging.DEBUG)
except Exception as e:
    print(f"Error starting bot: {e}")



