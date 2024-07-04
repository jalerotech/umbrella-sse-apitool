import requests
import logging
from Auth.CreateAuth import get_access_token

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def fetchOverrideSwgSetting(API_KEY_ID, API_KEY, org_origin_data) -> list:
    """
    Gets the SWG-Enabled settings value if set. And creates if the parameter is non-existence.
    :param API_KEY_ID: API_KEY_ID
    :param API_KEY: API_KEY
    :param origin_id: origin_id
    :param org_id: org_id
    :return: List -> e.g. [{"originId": 627310948, "name": "SWGEnabled", "value": "1", "modifiedAt": "2024-06-11T12:18:17Z"}]
    """
    logger = logging.getLogger('Running fetchOverrideSwgSetting')
    access_token, ret_org = get_access_token(API_KEY_ID, API_KEY, org_origin_data['org'])

    url = "https://api.umbrella.com/deployments/v2/deviceSettings/SWGEnabled/list"

    payload = f'''{{"originIds": {org_origin_data['list_of_origins']} }}'''

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.request('POST', url, headers=headers, data=payload)
    if response.status_code == 200:
        if type(response.json()) == dict:
            logger.info('No Override set, creating it.')
            return setOverrideSwgSetting(API_KEY_ID, API_KEY, origin_id, org_id)
        else:
            return response.json()


def setOverrideSwgSetting(API_KEY_ID, API_KEY, origin_id, org_id):
    logger = logging.getLogger('Running setOverrideSwgSetting')
    access_token, ret_org = get_access_token(API_KEY_ID, API_KEY, org_id)

    url = "https://api.umbrella.com/deployments/v2/deviceSettings/SWGEnabled/set"
    payload = f'''{{"originIds": [ {origin_id} ], "value": "1"}}'''
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.request('POST', url, headers=headers, data = payload)
    if response.status_code == 200:
        logger.info(f"SWG-enabled override set for org {org_id} and originId {origin_id}.")
        return response.json()


if __name__ == '__main__':
    # API_KEY_ID = "2e532d736f9d418c968a129a91920d3d"
    # API_KEY = "5425e7dedf5b4e0391cb745e3040ba77"
    origin_id = 620296473
    org_id = 8140857
    # JaleroDMZ lab keys
    API_KEY_ID = 'f04fd75db50c48f58043b9500e07a1af'
    API_KEY = 'd75dd5e410cc42d0ac535cd2795ba5bb'
    fetchOverrideSwgSetting(API_KEY_ID, API_KEY, origin_id, org_id)
    