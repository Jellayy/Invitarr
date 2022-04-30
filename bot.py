import discord
import logging
from configparser import ConfigParser


# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s:%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logging.getLogger('discord')


# Initialize discord.py client
client = discord.Client()


# On login
@client.event
async def on_ready():
    logging.info(f'Logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('Hello'):
        await message.channel.send(f'Hello {message.author}!')


# Run discord.py client
parser = ConfigParser()
parser.read('config.ini')
client.run(parser.get('Discord', 'api key'))
