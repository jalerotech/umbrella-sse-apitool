import requests
import logging
from data_file import api_key_data
from Auth.CreateAuth import get_access_token


def get_tunnels(access_token) -> (bool, list):
    """
    Queries UmbrellaApiTool for the existing tunnels created on your org and deployment
    :param :
    :return: tunnel id -> int
    """

    logger = logging.getLogger('Running custom UmbrellaApiTool get_tunnels Script. ')
    logger.info(' Fetching Existing tunnels from your org and deployment. ')

    url = "https://api.umbrella.com/deployments/v2/tunnels"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        # Checking the response if there's only one tunnel on the deployment
        if len(resp.json()) < 1:
            print("There are no Tunnel in your org.")
            tunnels_found = False
            return tunnels_found

        else:
            tunnels_ids = []
            # Otherwise loop through the list of tunnel data in response
            for tunnel in resp.json():
                tunnels_ids.append(tunnel['id'])
                print(f"Found a Tunnel with the following data -> id {tunnel['id']}")
            return tunnels_ids
    else:
        logger.info(f"Get_tunnel function failed with {resp.status_code}")


if __name__ == "__main__":
    access_token = get_access_token(api_key_data["API_KEY_ID"], api_key_data["API_KEY"])
    get_tunnels(access_token)
