import discord


async def ask_for_email():
    embed = discord.Embed(
        color=discord.Color.blue(),
        title="Plex Share Invite",
        description="Please provide your Plex account email address to be invited to the share"
    )
    embed.set_footer(text="This request will expire in 24 hours")
    return embed


async def email_success():
    embed = discord.Embed(
        color=discord.Color.green(),
        title="Invite Sent",
        description="Check your Plex account for a friend request. An email with overseerr login information has also been sent, login as an overseerr user for requests"
    )
    return embed


async def invalid_email():
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Invalid Email Provided",
        description="Please reply with a valid email address"
    )
    return embed


async def email_timeout():
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Plex Invite Timeout",
        description="No valid email was provided within 24 hours, please contact a server administrator to be re-invited"
    )
    return embed


async def email_in_use():
    embed = discord.Embed(
        color=discord.Color.red(),
        title="Email In Use",
        description="This email is already in use by another user on this server, please contact your administrator"
    )
    return embed


async def dm_cancelled():
    embed = discord.Embed(
        color=discord.Color.red(),
        title="DM Cancelled",
        description="Signup cancelled, feel free to readd the associated role at any time to be reinvited"
    )
    return embed
