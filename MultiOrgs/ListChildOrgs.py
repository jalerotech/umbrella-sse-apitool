import requests
import logging
# from data_file import api_key_data
from Auth.CreateAuth import get_access_token

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def returnChildOrgs(API_KEY_ID, API_KEY) -> list:
    logger = logging.getLogger('returnChildOrgs')
    """
    Uses the Multi-org API keys to return list of child-orgs from the multi-org console.
    :param: None
    :return:list -> of dict of all child-orgs
    """
    logger.info(f"Getting child-orgs from multi-org console")
    # access_token = get_access_token(api_key_data["API_KEY_ID"], api_key_data["API_KEY"], org_id=None)
    access_token, org_id_ret = get_access_token(API_KEY_ID, API_KEY, org_id=None)

    logger = logging.getLogger('Running returnChildOrgs function')
    logger.info(f"Getting Child orgs Multi-org console.")

    url = "https://api.umbrella.com/admin/v2/managed/customers"
    list_of_child_orgs = []
    if access_token:
        payload = None
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        try:
            resp = requests.get(url, headers=headers, data=payload)
            response = resp.json()
            for child_org in response:
                list_of_child_orgs.append(child_org['customerId'])
            return list_of_child_orgs
        except Exception as e:
            logger.info(f"Error occurred with error {e.args}")


if __name__ == '__main__':
    returnChildOrgs(API_KEY_ID=None, API_KEY=None)
