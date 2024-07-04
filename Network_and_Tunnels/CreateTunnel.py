import requests
import json
import logging
from Auth.CreateAuth import get_access_token
from data_file import api_key_data, tunnel_data

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def create_tunnel(data) -> bool:
    """
    Creates a Tunnel on your org deployment using the data provided
    :param data: tunnel data
    :return:
    """

    logger = logging.getLogger('Running custom UmbrellaApiTool create_tunnel Script ')
    logger.info('Creating IPsec Tunnel identity with the tunnel data provided: ')

    tunnel_created = False
    # Gets the access token required for further requests
    access_token = get_access_token(api_key_data["API_KEY_ID"], api_key_data["API_KEY"])

    # Gets the SiteOriginID from your deployment
    origin_id = _get_site_origin_id(access_token)

    url = "https://api.umbrella.com/deployments/v2/tunnels"

    # Updates the tunnel_data provided, using data here for simplicity
    data.update({"siteOriginId": origin_id})

    # Jsonify the data so the API endpoint can accept the request and data input type
    json_dict = json.dumps(data, indent=4)

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    resp = requests.post(url, headers=headers, data=json_dict)

    resp_status = resp.status_code

    if resp_status == 200:
        print(f"Tunnel {data['name']} has been created on your deployment.")
        tunnel_created = True
    else:
        print(resp.text)

    return tunnel_created


def _get_site_origin_id(access_token):
    logger = logging.getLogger('Running "_get_site_origin_id" script...')
    logger.info('Getting SiteOriginID to create Tunnel...')

    url = "https://api.umbrella.com/deployments/v2/sites"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    resp = requests.get(url, headers=headers)
    origin_id = json.loads(resp.text)[0]["originId"]
    return origin_id


if __name__ == "__main__":
    create_tunnel(tunnel_data)
