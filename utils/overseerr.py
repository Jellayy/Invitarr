import requests
import logging


def build_headers(overseerr_api):
    headers = {
        'accept': 'application/json',
        'X-Api-Key': overseerr_api,
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
    }
    return headers


def create_user(overseerr_api, overseerr_server, user_email):
    logging.info(f"OVERSEERR: Creating account for: {user_email}")
    json_data = {
        'email': user_email,
        'username': user_email,
    }
    r = requests.post(overseerr_server+'/api/v1/user', headers=build_headers(overseerr_api), json=json_data)

    if r.status_code == 409:
        logging.error(f"OVERSEERR: User: {user_email} already exists")
        return None
    elif r.status_code == 201:
        logging.info(f"OVERSEERR: User: {user_email} successfully created with ID: {r.json()['id']}")
        return r.json()['id']
    else:
        logging.error(f"OVERSEERR: Creating User: {user_email} failed with unhandled status code: {r.status_code} json: {r.json()}")
        return None


def delete_user(overseerr_api, overseerr_server, user_id):
    logging.info(f"OVERSEERR: Removing account ID: {user_id}")
    r = requests.delete(f"{overseerr_server}/api/v1/user/{user_id}", headers=build_headers(overseerr_api))

    if r.status_code == 200:
        logging.info(f"OVERSEERR: Deleted account ID: {user_id} successfully!")
        return True
    elif r.status_code == 404:
        logging.error(f"OVERSEERR: Cannot delete account ID: {user_id}, account does not exist.")
        return False
    else:
        logging.error(f"OVERSEERR: Account ID: {user_id} deletion failed with unhandled status code: {r.status_code} json: {r.json()}")
        return False
