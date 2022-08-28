import discord
from discord.ext import commands
import utils.db.db_driver as db_driver
import utils.plex as plex
import utils.overseerr as overseerr
import utils.embeds as embeds
import utils.utils as utils
import logging

global overseerr_server
global overseerr_api
global overseerr_enabled


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
                    # Remove User From Plex Share
                    if plex.remove_user(plex_server_account['account'], user_email):
                        if overseerr_enabled and user[5] != "None":
                            # Delete Overseerr Account
                            if overseerr.delete_user(overseerr_api, overseerr_server, user[5]):
                                await ctx.send(embed=await embeds.generic_success(f"User with email: {user_email} successfully removed from Plex and Overseerr"))
                                db_driver.delete_user(self.client.db_cur, self.client.db_con, user_email)
                            else:
                                await ctx.send(embed=await embeds.generic_failure(f"Successfully removed user with email: {user_email} from Plex share. However, Overseerr account deletion has failed. See logs for more info.\n\nUser has been removed from DB, please manually remove Overseerr account."))
                                db_driver.delete_user(self.client.db_cur, self.client.db_con, user_email)
                        else:
                            await ctx.send(embed=await embeds.generic_success(f"User with email: {user_email} successfully removed from Plex"))
                            db_driver.delete_user(self.client.db_cur, self.client.db_con, user_email)
                    else:
                        await ctx.send(embed=await embeds.generic_failure(f"Could not remove {user_email} from Plex share. See container logs for more info."))
        else:
            await ctx.send(embed=await embeds.generic_failure(f"email: {user_email} not found in DB"))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def force_delete_user(self, ctx, user_email):
        if db_driver.check_user_email(self.client.db_cur, user_email):
            user = db_driver.grab_user(self.client.db_cur, user_email)
            plex_share = "no change"
            overseerr_account = "no change"

            for plex_server_account in self.client.plex_connections:
                if plex_server_account['account'].email == user[2]:
                    if plex.remove_user(plex_server_account['account'], user_email):
                        plex_share = "deleted"

            if overseerr_enabled and user[5] != "None":
                if overseerr.delete_user(overseerr_api, overseerr_server, user[5]):
                    overseerr_account = "deleted"

            db_driver.delete_user(self.client.db_cur, self.client.db_con, user_email)

            await ctx.send(embed=await embeds.generic_success(f"Plex share: {plex_share}\nOverseerr account: {overseerr_account}\nDB listing: deleted"))
        else:
            await ctx.send(embed=await embeds.generic_failure(f"email: {user_email} not found in DB"))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_user(self, ctx, user: str = None, user_email: str = None, create_overseerr_account: str = "FALSE"):
        if user is None or user_email is None:
            await ctx.send(embed=await embeds.generic_failure("Missing Parameters\nUsage:\nadd_user @USER USER_EMAIL CREATE_OVERSEERR_ACCOUNT[optional, True]"))
        else:
            user = await self.client.fetch_user(user.replace("<@", "").replace(">", ""))
            user_name = user.name
            if overseerr_enabled and create_overseerr_account.upper() == "TRUE":
                if utils.add_user(self.client, user_email, user_name, True, overseerr_api, overseerr_server):
                    await ctx.send(embed=await embeds.generic_success("User added!"))
            else:
                if utils.add_user(self.client, user_email, user_name):
                    await ctx.send(embed=await embeds.generic_success("User added!"))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prune(self, ctx, account_email: str = None):
        if account_email is None:
            await ctx.send(
                embed=await embeds.generic_failure("Missing Parameters\nUsage:\ndry_prune account server_num"))
        else:
            # Check user input again
            account_exists = False
            for plex_connection in self.client.plex_connections:
                if plex_connection['account_email'] == account_email:
                    account_exists = True

                    users_to_prune = []
                    all_users = plex.get_users(plex_connection['account'])
                    for user in all_users:
                        # statement for debug, remove in prod
                        print(db_driver.grab_user(self.client.db_cur, user['email']))
                        # this line is necessary to prevent crashes when db_driver screws up
                        if db_driver.grab_user(self.client.db_cur, user['email']) is not None:
                            user_server_id = db_driver.grab_user(self.client.db_cur, user['email'])[4]
                            for server in plex_connection['servers']:
                                if server.machineIdentifier == user_server_id:
                                    if not server.history(accountID=user['id']):
                                        users_to_prune.append(user['email'])

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
                                                db_driver.delete_user(self.client.db_cur, self.client.db_con,
                                                                      user_email)
                                            else:
                                                await ctx.send(embed=await embeds.generic_failure(
                                                    f"Successfully removed user with email: {user_email} from Plex share. However, Overseerr account deletion has failed. See logs for more info.\n\nUser has been removed from DB, please manually remove Overseerr account."))
                                                db_driver.delete_user(self.client.db_cur, self.client.db_con,
                                                                      user_email)
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
