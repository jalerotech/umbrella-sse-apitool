import json
import requests
from requests.auth import HTTPBasicAuth
import logging
import base64
# from data_file import api_key_data
import hashlib

AuthURL = "https://api.umbrella.com/auth/v2/token"
server = "https://api.umbrella.com"
# API_KEY_ID = api_key_data["API_KEY_ID"]
# API_KEY = api_key_data["API_KEY"]

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def get_access_token(api_key_id, api_key, org_id):

    """
    Creates the access token string using the API KEY ID and API KEY provided.

    :param org_id: child-org_id
    :param api_key_id: API KEY ID
    :param api_key: API KEY
    :return: access_token str
    """

    logger = logging.getLogger('Running custom UmbrellaApiTool get_access_token Script ')
    logger.info('Generating Auth Token using API key.')

    authurl = "https://api.umbrella.com/auth/v2/token"

    auth_data = HTTPBasicAuth(api_key_id, api_key)
    # resp = {}
    if org_id:
        resp = _retOrgIdAuth(org_id, authurl, auth_data)
    else:
        resp = _retAuth(authurl, auth_data)
    access_token = ''
    validity = ''
    try:
        access_token = resp["access_token"]
        validity = resp["expires_in"]
    except KeyError as e:
        logger.info(f"Error occurred as  -> {e.args}")

    # Additional data to present to the user about their org and potentially the rights associated with their API key.
    # parses out the part of the JWT containing the access token and then create a list by splitting
    # the string using the dot marker.
    if access_token:
        org_from_access_token = access_token.split('.')[1]

        # Padding is required here to avoid getting incorrect padding error from the base64 decoding
        padded_org_from_access_token = f'{org_from_access_token}{"=="}'

        # Decoding the parsed data from base64 string to dict
        org_from_access_token_decoded = json.loads(base64.b64decode(padded_org_from_access_token).decode('utf-8'))
        org_id = org_from_access_token_decoded['sub'].split("/")[1]

        logger.info(f'Access Token created => {access_token}.')
        logger.info(f'Note that the token created is valid for {validity} seconds.')
        logger.info(f'The Access token is associated with your org ID => {org_id}')

        return access_token, org_id


def _retOrgIdAuth(org_id, authurl, auth_data):
    logger = logging.getLogger("_retOrgIdAuth")
    payload = {'grant_type=client_credentials'}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Umbrella-OrgId": f"{org_id}"
    }
    try:
        re = requests.get(url=authurl, auth=auth_data, headers=headers, data=payload)
        resp = re.json()
        return resp
    except Exception as e:
        logger.info(f"Request Failed with error -> {e.args}")


def _retAuth(authurl, auth_data):
    logger = logging.getLogger("_retAuth")
    try:
        re = requests.get(url=authurl, auth=auth_data, data=None)
        resp = re.json()
        return resp
    except Exception as e:
        logger.info(f"Request Failed with error -> {e.args}")


if __name__ == "__main__":
    get_access_token(API_KEY_ID, API_KEY, org_id=None)