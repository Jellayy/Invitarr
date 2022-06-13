import requests
import logging


def create_user(overseerr_api, overseerr_server, user_email):
    headers = {
        'accept': 'application/json',
        'X-Api-Key': overseerr_api,
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
    }

    json_data = {
        'email': user_email,
        'username': user_email,
    }

    response = requests.post(overseerr_server, headers=headers, json=json_data)

    logging.info(response.json())
    logging.info('Added User to overseerr')
    return True


