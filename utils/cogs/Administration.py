import discord
from discord.ext import commands
import utils.db.db_driver as db_driver
import utils.plex as plex
import utils.overseerr as overseerr


global overseerr_server
global overseerr_api


class Administration(commands.Cog):
    # Init Cog
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def delete_user(self, ctx, user_email):
        if db_driver.check_user_email(self.client.db_cur, user_email):
            user = db_driver.grab_user(self.client.db_cur, user_email)
            for plex_server_account in self.client.plex_connections:
                if plex_server_account['account'].email == user[2]:
                    plex.remove_user(plex_server_account['account'], user_email)
            if user[5] != "None":
                overseerr.delete_user(overseerr_api, overseerr_server, user[5])
            db_driver.delete_user(self.client.db_cur, self.client.db_con, user_email)
            await ctx.send(f"User with email: {user_email} successfully deleted")
        else:
            await ctx.send(f"ERROR: email: {user_email} not found in DB")


def setup(client):
    # Load overseer config
    global overseerr_server
    overseerr_server = client.parser.get('Overseerr Settings', 'Overseerr Server')
    global overseerr_api
    overseerr_api = client.parser.get('Overseerr Settings', 'API Key')

    # Add Cog
    client.add_cog(Administration(client))
