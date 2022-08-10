from discord.ext import commands
from configparser import ConfigParser
import logging
import utils.utils as utils
import utils.plex as plex
import utils.db.db_driver as db_driver
import utils.overseerr as overseerr


global monitored_role_name


class RoleMonitoring(commands.Cog):
    # Init Cog
    def __init__(self, client):
        self.client = client

    # Monitors a given role for new users and invites them to plex share
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        # Obtain monitored role object from server
        monitored_role = None
        for role in after.guild.roles:
            if role.name == monitored_role_name:
                monitored_role = role
        if monitored_role is None:
            logging.error("DISCORD: Unable to find monitored role in server")

        # Check obtained role
        for role in after.roles:
            if role not in before.roles:
                logging.info(f"DISCORD: User: {after.name} gained role: {role.name}")
                if role == monitored_role:
                    if db_driver.search_user(self.client.db_cur, after.name):
                        logging.info(f"SQLITE3: {after.name} already in DB, skipping")
                    else:
                        logging.info(f"DISCORD: {after.name} gained monitored role, opening DM")
                        # Open DM to obtain email
                        user_email = await utils.get_user_email(self.client, after)
                        # Find the least crowded server
                        optimal_server = plex.find_optimal_server(self.client.plex_connections)
                        # Send Plex invite email
                        if plex.add_user(optimal_server['account'], user_email, optimal_server['server']) & overseerr.create_user(overseerr_api, overseerr_server, user_email):
                            # Add user to DB
                            db_driver.add_user(self.client.db_con, self.client.db_cur, after.name, user_email, optimal_server['account'].email, optimal_server['server'].friendlyName, optimal_server['server'].machineIdentifier, "True")


def setup(client):
    # Load monitored role name from config
    global monitored_role_name
    monitored_role_name = client.parser.get('Role Monitoring', 'monitored role')
    global overseerr_server
    overseerr_server = client.parser.get('Overseerr Settings', 'Overseerr Server')
    global overseerr_api
    overseerr_api = client.parser.get('Overseerr Settings', 'API Key')

    # Add Cog
    logging.info("DISCORD: Adding cog: RoleMonitoring")
    client.add_cog(RoleMonitoring(client))
    logging.info("DISCORD: RoleMonitoring Cog loaded!")
    logging.info(f"DISCORD: Monitored role name is: {monitored_role_name}")
