from plexapi.exceptions import NotFound
from plexapi.exceptions import BadRequest
import logging


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
