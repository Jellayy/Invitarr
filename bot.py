from os.path import exists
import sys
import discord
from discord.ext import commands
import logging
from configparser import ConfigParser
from utils.config import config_gen
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

# On first run, generate config file and exit
if not exists('/config/config.ini'):
    logging.error("INIT: No config file found, generating empty config file...")
    config_gen.gen_empty_config()
    logging.info("INIT: Empty config generated in /config path. Please fill config.ini before restarting bot.")
    sys.exit()
else:
    # Load Config file
    logging.info("INIT: Config file found")
    parser = ConfigParser()
    parser.read('/config/config.ini')
    # Check if config file is populated before continuing
    if parser.get('Discord', 'bot token') == "" or parser.get('Plex Account 0', 'user') == "" or parser.get('Plex Account 0', 'password') == "" or parser.get('Plex Account 0', 'server 0') == "":
        logging.error("INIT: Config file not populated. Please fill config.ini before restarting bot.")
        sys.exit()

# Initialize discord.py client
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='.', intents=intents)

# Pass config parser to client
client.parser = parser

# Initialize Plex API
client.plex_connections = plex.create_connections(client.parser)

# Initialize db
logging.info("SQLITE3: Connecting to DB")
client.db_con = sqlite3.connect('/config/invitarr.db')
client.db_cur = client.db_con.cursor()
logging.info("SQLITE3: Connected!")
db_driver.init_user_table(client.db_con, client.db_cur, client.plex_connections)

# Load cogs
if client.parser.get('Role Monitoring', 'enable') == '1':
    logging.info(f'INIT: Role Monitoring enabled in config')
    client.load_extension('utils.cogs.RoleMonitoring')
client.load_extension('utils.cogs.DBManager')
client.load_extension('utils.cogs.Administration')


# On login
@client.event
async def on_ready():
    logging.info(f'DISCORD: Logged in to Discord as {client.user}')


# Run discord.py client
client.run(parser.get('Discord', 'bot token'))
