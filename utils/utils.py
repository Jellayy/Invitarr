from asyncio import TimeoutError
import utils.embeds as embeds
import re
import utils.db.db_driver as db_driver
import utils.plex as plex
import utils.overseerr as overseerr


# Creates a DM conversation with a discord user to obtain their email
async def get_user_email(client, user):
    user_email = None
    await user.send(embed=await embeds.ask_for_email())
    while user_email is None:
        def check_sender(m):
            return m.author == user

        try:
            message = await client.wait_for('message', timeout=86400, check=check_sender)
            if message.content.lower() == "cancel":
                await user.send(embed=await embeds.dm_cancelled())
                return None
            elif check_email(message.content):
                if db_driver.check_user_email(client.db_cur, message.content):
                    await user.send(embed=await embeds.email_in_use())
                else:
                    user_email = message.content
                    await user.send(embed=await embeds.email_success())
            else:
                await user.send(embed=await embeds.invalid_email())
        except TimeoutError:
            await user.send(embed=await embeds.email_timeout())
    return user_email


# Global method for adding user to share and overseerr
def add_user(client, user_email, user_name, overseerr_enabled: bool = False, overseerr_api: str = None,
             overseerr_server: str = None):
    # Find the least crowded server
    optimal_server = plex.find_optimal_server(client.plex_connections)
    # Send Plex invite email
    if plex.add_user(optimal_server['account'], user_email, optimal_server['server']):
        if overseerr_enabled:
            overseerr_account_id = overseerr.create_user(overseerr_api, overseerr_server, user_email)
            if overseerr_account_id is not None:
                # Add user to DB
                db_driver.add_user(client.db_con, client.db_cur, user_name, user_email, optimal_server['account'].email,
                                   optimal_server['server'].friendlyName, optimal_server['server'].machineIdentifier,
                                   overseerr_account_id)
            else:
                # Add user to DB with no overseer
                db_driver.add_user(client.db_con, client.db_cur, user_name, user_email, optimal_server['account'].email,
                                   optimal_server['server'].friendlyName, optimal_server['server'].machineIdentifier,
                                   "None")
        else:
            # Add user to DB with no overseer
            db_driver.add_user(client.db_con, client.db_cur, user_name, user_email, optimal_server['account'].email,
                               optimal_server['server'].friendlyName, optimal_server['server'].machineIdentifier,
                               "None")

        return True


# Regex method to validate emails
def check_email(address):
    email_filter = "(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"
    return re.match(email_filter, address.lower())

