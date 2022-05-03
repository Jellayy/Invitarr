import discord
from discord.ext import commands
import logging
from configparser import ConfigParser
from plexapi.myplex import MyPlexAccount
import sqlite3
import utils.db.db_driver as db_driver


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
logging.info(f"PLEXAPI: Logging in to: {parser.get('Plex', 'email')}")
client.plex_account = MyPlexAccount(parser.get('Plex', 'email'), parser.get('Plex', 'password'))
logging.info(f"PLEXAPI: Logged in!")
logging.info(f"PLEXAPI: Connecting to server: {parser.get('Plex', 'server')}")
client.plex_server_connection = client.plex_account.resource(parser.get('Plex', 'server')).connect()
logging.info(f"PLEXAPI: Connected!")

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
