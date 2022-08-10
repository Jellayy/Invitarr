from plexapi.myplex import MyPlexAccount
from plexapi.exceptions import NotFound, BadRequest
import logging
import time


def plex_login(user, password):
    logging.info(f"PLEXAPI: Logging into Account: {user}")
    success = False
    while not success:
        try:
            plex_account = MyPlexAccount(user, password)
            success = True
        except BadRequest as e:
            logging.error(f"PLEXAPI: Login to account: {user} failed with status: {e}, retrying in 30sec")
            time.sleep(30)
    logging.info(f"PLEXAPI: Logged in!")

    return plex_account


def create_connections(parser):
    plex_connections = []
    # For Each Plex Account in Config
    for x in range(int(parser.get('Plex Accounts', 'num accounts'))):
        # Log into account
        plex_account = plex_login(parser.get(f'Plex Account {x}', 'user'), parser.get(f'Plex Account {x}', 'password'))
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


def find_optimal_server(plex_connections):
    lowest_users = 999
    optimal_server = {"account": None, "server": None}
    for account in plex_connections:
        for server in account['servers']:
            if server is not None:
                if len(server.systemAccounts()) < lowest_users:
                    lowest_users = len(server.systemAccounts())
                    optimal_server['account'] = account['account']
                    optimal_server['server'] = server
    return optimal_server


def add_user(plex_account, user_email, server_connection):
    try:
        logging.info(f"PLEXAPI: Inviting {user_email} to {server_connection.friendlyName}")
        plex_account.inviteFriend(user=user_email, server=server_connection)
        logging.info(f"PLEXAPI: Invited {user_email} to {server_connection.friendlyName}")
        return True
    except BadRequest:
        logging.error(f'PLEXAPI: Already sharing with {user_email} on server {server_connection.friendlyName}')
        return False


def remove_user(plex_account, user_email):
    try:
        logging.info(f"PLEXAPI: Removing {user_email} from shares on account: {plex_account.email}")
        plex_account.removeFriend(user_email)
        logging.info(f"PLEXAPI: Removed {user_email} from shares on account: {plex_account.email}")
        return True
    except NotFound:
        logging.error(f"PLEXAPI: Cannot remove {user_email} from shares on account: {plex_account.email}: not sharing with this user")
        return False
