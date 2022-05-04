from plexapi.myplex import MyPlexAccount
from plexapi.exceptions import NotFound, BadRequest
import logging


def create_connections(parser):
    plex_connections = []
    # For Each Plex Account in Config
    for x in range(int(parser.get('Plex Accounts', 'num accounts'))):
        # Log into account
        logging.info(f"PLEXAPI: Logging into Account: {parser.get(f'Plex Account {x}', 'user')}")
        plex_account = MyPlexAccount(parser.get(f'Plex Account {x}', 'user'), parser.get(f'Plex Account {x}', 'password'))
        logging.info(f"PLEXAPI: Logged in!")
        # Store account
        plex_connections.append({"account": plex_account, "servers": []})

        # For Each Server in Plex Account
        for y in range(int(parser.get(f'Plex Account {x}', 'num servers'))):
            try:
                # Connect to server
                logging.info(f"PLEXAPI: Connecting to server: {parser.get(f'Plex Account {x}', f'server {y}')}")
                server_connection = plex_account.resource(parser.get(f'Plex Account {x}', f'server {y}')).connect()
                logging.info(f"PLEXAPI: Connected!")
                # Store connection
                plex_connections[x]['servers'].append(server_connection)
            except NotFound:
                logging.error(f"PLEXAPI: Cannot find server {parser.get(f'Plex Account {x}', f'server {y}')}")
                plex_connections[x]['servers'].append(None)
    return plex_connections


def add_user(plex_account, user_email, server_connection):
    try:
        logging.info(f"PLEXAPI: Inviting {user_email}")
        plex_account.inviteFriend(user=user_email, server=server_connection)
        logging.info(f"PLEXAPI: Invited {user_email}")
        return True
    except BadRequest:
        logging.error(f'PLEXAPI: Already sharing with {user_email}')
        return False


def remove_user(plex_account, user_email):
    try:
        logging.info(f"PLEXAPI: Removing friend {user_email}")
        plex_account.removeFriend(user=user_email)
        logging.info(f"PLEXAPI: {user_email} removed")
        return True
    except NotFound:
        logging.error(f"PLEXAPI: {user_email} not found in friends list")
        return False
