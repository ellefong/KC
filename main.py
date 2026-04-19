import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import dotenv
import os
from PIL import Image
import image
import random
import asyncio

# This file is for the bot to run based on imput

#variables
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
dotenv.load_dotenv()

handler = logging.FileHandler(filename='dicord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
guessing_has_begun = False #check if user has started guessing

# undercover = "Kraken" # this is for the Roles portion if we want it 

active_games = {}  # Dict to store active guessing games {user_id: target_number}


@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")

# When user types certain messages...
@bot.event
async def on_message(message):

    if message.author == bot.user:
        return
    
    play_again = True
    # and message.author.id not in active_games
    if "kraken" in message.content.lower(): 
        print("Guessing game queued!")
        #print(guessing_has_begun)
        #print("Got past guessing_has_begun without printing")
        #if guessing_has_begun is False:
        random_guessed_number = random.randint(1, 10)
        
        while play_again == True:
            print(f'Guessed Number: {random_guessed_number}')


            active_games[message.author.id] = random_guessed_number
            # await message.delete()  
            await message.channel.send("Ok!!! Guess a number from 1 to 10")
        # return  # Prevent processing this message further

            if message.author.id in active_games:
                try:

                    guess_msg = await bot.wait_for('message', 
                                      check=lambda m: m.author == message.author and m.channel == message.channel,
                                      timeout=30)

                    guess = int(guess_msg.content.strip())
                    #guessing_has_begun = True
                    if guess == active_games[message.author.id]:
                        await message.channel.send("Congrats!... I guess... whatever. Want to play again? Yes/No")
                        print("this correct guess if statement is running")
                        await message.channel.send(file=image.return_image()) 
                        response = await bot.wait_for('message',
                                         check=lambda m: m.author == message.author,
                                         timeout=30)
                        try:
                            if response.content.strip() == "Yes" or response.content.strip() == "yes" or response.content.strip() == "Y" or response.content.strip() == "y" or response.content.strip() == "ya" or response.content.strip() == "sure":
                                play_again = True
                                random_guessed_number = random.randint(1, 10)
                                #guessing_has_begun = False
                            elif response.content.strip() == "No" or response.content.strip() == "no" or response.content.strip() == "n" or response.content.strip() == "N" or response.content.strip() == "no thanks" or response.content.strip() == "No thanks" or response.content.strip() == "Not right now":
                                play_again = False
                                await response.channel.send("Sayonara suckaaaaaaaaaaaa")
                            else:
                                await response.channel.send("I said Yes or No, but I'll take that as a No. Goodbye!")
                                play_again = False
                        except ValueError:
                            await response.channel.send("I said Yes or No, but I'll take that as a No. Goodbye!")
                            play_again = False
                        del active_games[message.author.id]
                    elif 1 <= guess <= 10:
                        await message.channel.send("Nuh uh")
                        gif_file = image.return_gif()
                        await message.channel.send(file=gif_file) 
                    else:
                        await message.channel.send("buddy I said 1 through 10")
                except ValueError:
                    pass  
    

# Code to Debug if images don't load
    if "damn" in message.content.lower(): # Note add an array of curse words later
    # Past used words incase it doesnt work: shit, fuck, puto, PENDEJO, 
        await message.delete()
        await message.channel.send(f"{message.author.mention} DO NOT.")
    if "test image" in message.content.lower(): # author types test image
        await message.channel.send(file=image.return_image()) #or
        await message.channel.send(f"{message.author.mention} this is running.")
    if "test gif" in message.content.lower():
        print("Test GIF triggered!") # Check if the 'if' statement works
        
        try:
            gif_file = image.return_gif()
            print(f"File created: {gif_file}")
            await message.channel.send(file=gif_file)
            print("File sent successfully!")
        except Exception as e:
            print(f"Error inside the GIF logic: {e}")
        
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

async def play_audio_in_channel(channel, audio):
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=audio))
    # Sleep while audio is playing??
    while vc.is_playing():
        await asyncio.sleep(.1)
    await vc.disconnect()

@bot.command()
async def sound(ctx):
    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.send("Please enter a voice channel: ")
        return 
    
    await play_audio_in_channel(voice_channel, "audio.mp3")

    await ctx.message.delete()
   
    

    
##image stuff
# await ctx.message.channel.send(file=discord.File('path/to/image.png')) #or
# await ctx.message.channel.send(url='string')

try:
    bot.run(token, log_handler=handler, log_level=logging.DEBUG)
except Exception as e:
    print(f"Error starting bot: {e}")



