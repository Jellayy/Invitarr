import discord
from discord.ext import commands
import logging
from configparser import ConfigParser
from utils import plex
from utils.db import db_driver
import sqlite3


# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s:%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logging.getLogger('discord.client').disabled = True
logging.getLogger('discord.gateway').disabled = True
logging.getLogger('plexapi').disabled = True

# Load config
parser = ConfigParser()
parser.read('config.ini')

# Initialize discord.py client
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='.', intents=intents)

# Initialize db
logging.info("SQLITE3: Connecting to DB")
client.db_con = sqlite3.connect('utils/db/users.db')
client.db_cur = client.db_con.cursor()
logging.info("SQLITE3: Connected!")
db_driver.init_user_table(client.db_con, client.db_cur)

# Initialize Plex API
client.plex_connections = plex.create_connections(parser)

# Load cogs
if parser.get('Role Monitoring', 'enable') == '1':
    logging.info(f'DISCORD: Role Monitoring enabled')
    client.load_extension('utils.cogs.RoleMonitoring')
client.load_extension('utils.cogs.DBManager')


# On login
@client.event
async def on_ready():
    logging.info(f'DISCORD: Logged in to Discord as {client.user}')


# Run discord.py client
client.run(parser.get('Discord', 'bot token'))
