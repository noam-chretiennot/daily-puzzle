import discord
from discord.ext import commands
from Core import Core
from dotenv import load_dotenv
import os
from datetime import datetime
import time
import asyncio

#Bot permissions
default_intents = discord.Intents.default()
default_intents.members = True
default_intents.message_content=True

#Creation of the bot named client
client = commands.Bot(command_prefix="!",intents = default_intents)
Daily_puzzle = Core(client)


@client.event
async def on_ready():
    print("Le bot est prêt")
    while True:
        await client.loop.create_task(Daily_puzzle.sending_puzzle())
        time.sleep(24*3600)
    

@client.command()
async def ping(ctx):
    """Get the lantency of the bot"""
    latency = client.latency
    await ctx.send(latency)

# Run the bot
load_dotenv()

TOKEN = os.getenv('TOKEN') # Get the token from the .env file
client.run(TOKEN)