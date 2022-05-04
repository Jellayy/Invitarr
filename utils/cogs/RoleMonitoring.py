from discord.ext import commands
from configparser import ConfigParser
import logging
import utils.utils as utils
import utils.plex as plex
import utils.db.db_driver as db_driver


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

        # Check for monitored role
        if monitored_role in after.roles and monitored_role not in before.roles:
            logging.info(f"DISCORD: {after.name} given monitored role, opening DM")
            # Open DM to obtain email
            user_email = await utils.get_user_email(self.client, after)
            # Find the least crowded server
            optimal_server = plex.find_optimal_server(self.client.plex_connections)
            # Send Plex invite email
            if plex.add_user(optimal_server['account'], user_email, optimal_server['server']):
                # Add user to DB
                db_driver.add_user(self.client.db_con, self.client.db_cur, after.name, user_email, optimal_server['server'].friendlyName)


def setup(client):
    # Load monitored role name from config
    parser = ConfigParser()
    parser.read('config.ini')
    global monitored_role_name
    monitored_role_name = parser.get('Role Monitoring', 'monitored role')

    # Add Cog
    client.add_cog(RoleMonitoring(client))
