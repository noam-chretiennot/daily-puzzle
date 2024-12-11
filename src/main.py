from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

from dailyPuzzleUtils import Core

#Bot permissions
default_intents = Intents.default()
default_intents.members = True
default_intents.message_content=True

#Creation of the bot named client
client = commands.Bot(command_prefix="!",intents = default_intents)
Daily_puzzle = Core(client)


@client.event
async def on_ready():
    """Start sending messages"""
    print("Le bot est prêt")
    await client.loop.create_task(Daily_puzzle.sending_puzzle())



@client.command()
async def ping(ctx):
    """Get the lantency of the bot"""
    latency = client.latency
    await ctx.send(latency)

# Run the bot
load_dotenv()

TOKEN = getenv('TOKEN') # Get the token from the .env file
client.run(TOKEN)