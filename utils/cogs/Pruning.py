import discord
from discord.ext import commands
import utils.db.db_driver as db_driver
import utils.plex as plex
import utils.overseerr as overseerr
import utils.embeds as embeds
import utils.utils as utils
import logging


class Pruning(commands.Cog):
    # Init Cog
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prune(self, ctx, account_email: str = None):
        if account_email is None:
            await ctx.send(embed=await embeds.generic_failure("Missing Parameters\nUsage:\ndry_prune account server_num"))
        else:
            # Check user input again
            account_exists = False
            for plex_connection in self.client.plex_connections:
                if plex_connection['account_email'] == account_email:
                    account_exists = True

                    users_to_prune = []
                    all_users = plex.get_users(plex_connection['account'])
                    for user in all_users:
                        user_server_id = db_driver.grab_user(self.client.db_cur, user['email'])[4]
                        for server in plex_connection['servers']:
                            if server.machineIdentifier == user_server_id:
                                if not server.history(account_id=user['id']):
                                    users_to_prune.append(user['id'])

                    # TODO: Generalize this method
                    for user_email in users_to_prune:
                        if db_driver.check_user_email(self.client.db_cur, user_email):
                            user = db_driver.grab_user(self.client.db_cur, user_email)
                            for plex_server_account in self.client.plex_connections:
                                if plex_server_account['account'].email == user[2]:
                                    # Remove User From Plex Share
                                    if plex.remove_user(plex_server_account['account'], user_email):
                                        if overseerr_enabled and user[5] != "None":
                                            # Delete Overseerr Account
                                            if overseerr.delete_user(overseerr_api, overseerr_server, user[5]):
                                                await ctx.send(embed=await embeds.generic_success(
                                                    f"User with email: {user_email} successfully removed from Plex and Overseerr"))
                                                db_driver.delete_user(self.client.db_cur, self.client.db_con, user_email)
                                            else:
                                                await ctx.send(embed=await embeds.generic_failure(
                                                    f"Successfully removed user with email: {user_email} from Plex share. However, Overseerr account deletion has failed. See logs for more info.\n\nUser has been removed from DB, please manually remove Overseerr account."))
                                                db_driver.delete_user(self.client.db_cur, self.client.db_con, user_email)
                                        else:
                                            await ctx.send(embed=await embeds.generic_success(
                                                f"User with email: {user_email} successfully removed from Plex"))
                                            db_driver.delete_user(self.client.db_cur, self.client.db_con, user_email)
                                    else:
                                        await ctx.send(embed=await embeds.generic_failure(
                                            f"Could not remove {user_email} from Plex share. See container logs for more info."))
                        else:
                            await ctx.send(embed=await embeds.generic_failure(f"email: {user_email} not found in DB"))


def setup(client):
    global overseerr_enabled
    overseerr_enabled = False
    if client.parser.get('Overseer Account Management', 'Enable') == '1':
        overseerr_enabled = True
        # Load overseer config
        global overseerr_server
        overseerr_server = client.parser.get('Overseerr Settings', 'Overseerr Server')
        global overseerr_api
        overseerr_api = client.parser.get('Overseerr Settings', 'API Key')

    # Add Cog
    logging.info("DISCORD: Adding cog: Administration")
    client.add_cog(Administration(client))
    logging.info("DISCORD: Administration Cog loaded!")