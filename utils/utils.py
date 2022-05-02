from asyncio import TimeoutError
import utils.embeds as embeds
import re


# Creates a DM conversation with a discord user to obtain their email
async def get_user_email(client, user):
    user_email = None
    await user.send(embed=await embeds.ask_for_email())
    while user_email is None:
        def check_sender(m):
            return m.author == user
        try:
            message = await client.wait_for('message', timeout=86400, check=check_sender)
            if check_email(message.content):
                user_email = message.content
                await user.send(embed=await embeds.email_success())
            else:
                await user.send(embed=await embeds.invalid_email())
        except TimeoutError:
            await user.send(embed=await embeds.email_timeout())
    return user_email


# Regex method to validate emails
def check_email(address):
    email_filter = '^(?:(?!.*?[.]{2})[a-zA-Z0-9](?:[a-zA-Z0-9.+!%-]{1,64}|)|\\"[a-zA-Z0-9.+!% -]{1,64}\\")@[a-zA-Z0-9][a-zA-Z0-9.-]+(.[a-z]{2,}|.[0-9]{1,})$'
    return re.match(email_filter, address)

