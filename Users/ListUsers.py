import requests
import logging
# from data_file import api_key_data
from Auth.CreateAuth import get_access_token

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def returnUsers(API_KEY_ID, API_KEY, org_id) -> dict:
    logger = logging.getLogger("returnUsers")
    """
    Produces a list of users per child-org or multi-org console.
    :param: org_id (child-org id -> if supplied)
    :return: list -> dict of users per child-org
    """
    if org_id:
        logger.info(f"Getting access token for child_org {org_id}")
        access_token, org_id_ret = get_access_token(API_KEY_ID, API_KEY, org_id)
        # access_token = get_access_token(api_key_data["API_KEY_ID"], api_key_data["API_KEY"], org_id)
    else:
        logger.info(f"Getting access token for multi-org")
        access_token, org_id_ret = get_access_token(API_KEY_ID, API_KEY, org_id=None)

    logger = logging.getLogger('Running returnUsers function')
    logger.info(f"Getting Users from org...")

    url = "https://api.umbrella.com/admin/v2/users"

    # Jsonify the dict for the request payload
    # json_dict = json.dumps(data, indent=4)
    payload = None
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    try:
        resp = requests.get(url, headers=headers, data=payload)
        response = resp.json()
        uer_data = {"ListOfUsers": {org_id: response}}
        return uer_data
    except Exception as e:
        logger.info(f"Request failed with {e.args}")


if __name__ == '__main__':
    returnUsers(API_KEY_ID=None, API_KEY=None, org_id=None)
