"""
Configure the bot and start daily sending of puzzles
"""
from os import getenv
import json
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

from daily_puzzle_utils import sending_puzzle

#Bot permissions
default_intents = Intents.default()
default_intents.members = True
default_intents.message_content=True

#Creation of the bot named client
client = commands.Bot(command_prefix="!",intents = default_intents)

server = getenv("SERVER")

with open(f'data/{server}_bot_info.json', 'r', encoding='utf-8') as f:
    temp = json.load(f)
    channels = temp["from_channel"]
    to_channel = temp["to_channel"]
    sending_hour = temp["sending_time"][0]
    sending_minute = temp["sending_time"][1]
    del temp


@client.event
async def on_ready():
    """Start sending messages"""
    await client.loop.create_task(
        sending_puzzle(client, channels, to_channel, sending_hour, sending_minute)
    )



@client.command()
async def ping(ctx):
    """Get the lantency of the bot"""
    latency = client.latency
    await ctx.send(latency)

# Run the bot
load_dotenv()

TOKEN = getenv('TOKEN') # Get the token from the .env file
client.run(TOKEN)
