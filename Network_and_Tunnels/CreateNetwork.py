import requests
import json
import logging
from Auth.CreateAuth import get_access_token
from data_file import api_key_data, payload_data

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def create_network(data) -> str:
    """
    Creates the network identity on your org deployment using the network data provided
    :param data: network data
    :return:
    """
    access_token = get_access_token(api_key_data["API_KEY_ID"], api_key_data["API_KEY"])

    logger = logging.getLogger('Running custom UmbrellaApiTool create_network Script ')
    logger.info('Creating network identity with the data provided: ')

    url = "https://api.umbrella.com/deployments/v2/networks"

    # Jsonify the dict for the request payload
    json_dict = json.dumps(data, indent=4)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    resp = requests.post(url, headers=headers, data=json_dict)

    # Note ensure you're running this script from a device behind the public IP address used in the payload data.
    # Need to add more conditions here to check for failed response and exception handling.
    resp_txt = resp.text
    if "The ip address you provided is outside of your verified cidr blocks" == json.loads(resp_txt)['message']:
        print(f"Your device is not behind the public IP {data['ipAddress']} "
              f"you're trying to add as a network identity on UmbrellaApiTool deployment.")
    else:
        print("Network identity created")

    return resp_txt


if __name__ == "__main__":
    create_network(payload_data)
