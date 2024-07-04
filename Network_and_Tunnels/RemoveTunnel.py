import requests
import logging
from Auth.CreateAuth import get_access_token
from data_file import api_key_data
from Network_and_Tunnels.GetTunnels import get_tunnels

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def remove_tunnel():
    """
    Removes IPSec Tunnel configuration using the tunnel id provided.
    This script first runs the get_tunnels() function to get the tunnel data from the deployment.
    Then executes the delete request.
    :return:
    """
    logger = logging.getLogger('Running "remove_tunnel" script...')

    # Gets the access token required for further requests
    access_token = get_access_token(api_key_data["API_KEY_ID"], api_key_data["API_KEY"])

    # Get Existing tunnels. This can be set to allow user to input tunnel_id if they have it at hand.
    tunnel_id_list = get_tunnels(access_token)
    tunnel_id = ''

    if (type(tunnel_id_list)) == bool:
        logger.info(f"Stopping the script since no Tunnels found in your deployment.")

    else:
        for tunl_id in tunnel_id_list:
            tunnel_id = tunl_id
            url = f"https://api.umbrella.com/deployments/v2/tunnels/{tunnel_id}"

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {access_token}"
            }

            if tunnel_id:
                logger.info(f' Removing Tunnel with ID -> "{tunnel_id}"  from your deployment.')
                resp = requests.delete(url, headers=headers)
                logger.info(f"{resp.json()['message']}")


if __name__ == "__main__":
    remove_tunnel()

