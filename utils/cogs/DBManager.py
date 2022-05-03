from discord.ext import commands
import utils.db.db_driver as db_driver


class DBManager(commands.Cog):
    # Init Cog
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def get_db(self, ctx):
        for row in db_driver.get_users(self.client.db_cur):
            await ctx.send(row)


def setup(client):
    # Add Cog
    client.add_cog(DBManager(client))
