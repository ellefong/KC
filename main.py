import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='dicord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

undercover = "Kracken" # this is for the Roles portion if we want it 

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
    if "damn" in message.content.lower(): # Note add an array of curse words later
    # Past used words incase it doesnt work: shit, fuck, puto, PENDEJO, 
        await message.delete()
        await message.channel.send(f"{message.author.mention} DO NOT.")

    await bot.process_commands(message) #this is needed to be called

# This prints a Hello Message from the bot if you use an "!"
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

# This assigns a role to someone
# However first you have to create the role through discord file
@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guilds.roles, name=undercover)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is not assigned to {secret_role}")
    else:
        await ctx.send("This role doesn't exist")

# This removes a role
@bot.command
async def assign(ctx):
    role = discord.utils.get(ctx.guilds.roles, name=undercover)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} had had the {secret_role} removed")
    else:
        await ctx.send("This role doesn't exist")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)



