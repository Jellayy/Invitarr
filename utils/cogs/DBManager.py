import discord
from discord.ext import commands
import utils.db.db_driver as db_driver


class DBManager(commands.Cog):
    # Init Cog
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def get_db(self, ctx):
        with open('utils/db/db_print.txt', 'w') as f:
            f.write("Discord User | User Plex Email | Server Plex Account | Server Name | Server ID | Overseer Connected\n")
            for row in db_driver.get_users(self.client.db_cur):
                f.write(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}\n")
        with open('utils/db/db_print.txt', 'rb') as file:
            await ctx.send(file=discord.File(file, 'utils/db/db_print.txt'))


def setup(client):
    # Add Cog
    client.add_cog(DBManager(client))
