import requests
import logging
from Auth.CreateAuth import get_access_token

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def fetchRoamingComputers(API_KEY_ID, API_KEY, org_id):
    """
    Produces a list of roaming computer that's part of the org by listing their originIds and the device information.
    :param API_KEY_ID: Key Id
    :param API_KEY: API key
    :param org_id: child-org id
    :return: List of Roaming client.
    """
    logger = logging.getLogger('Running fetchRoamingComputers')
    list_of_json_resp = []
    list_of_ret_org = []
    if len(org_id) > 1:
        for tenant in org_id:
            access_token, org_id_ret = get_access_token(API_KEY_ID, API_KEY, tenant)
            url = "https://api.umbrella.com/deployments/v2/roamingcomputers"

            payload = None

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {access_token}"
            }

            response = requests.request('GET', url, headers=headers, data=payload)
            print(response.__dict__)
            if response.status_code == 200:
                if len(response.json()) == 0:
                    logger.info(f"Returning device list returned Passing.")
                # if response.json():
                else:
                    if len(response.json()) > 0:
                        logger.info(f"Returning 'device_per_originId' list.")
                        list_of_ret_org.append(org_id_ret)
                        data_to_add = {'org_id': org_id_ret}
                        device_data = response.json()[0]
                        combined_dict = device_data.copy()
                        combined_dict.update(data_to_add)
                        list_of_json_resp.append(combined_dict)
                        # device_dict, list_of_originId = retListOfDevices(response.json(), org_id_ret)
            else:
                print(response.status_code)

        if list_of_json_resp and list_of_ret_org:
            # print(list_of_json_resp, list_of_ret_org)
            return retListOfDevices(list_of_json_resp, list_of_ret_org)

    else:
        access_token, org_id_ret = get_access_token(API_KEY_ID, API_KEY, org_id[0])
        url = "https://api.umbrella.com/deployments/v2/roamingcomputers"

        payload = None

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.request('GET', url, headers=headers, data=payload)
        if response.status_code == 200:
            if response.json() is []:
                logger.info(f"Returning device list returned Passing.")
            # if response.json():
            else:
                logger.info(f"Returning 'device_per_originId' list.")
                # retListOfDevices(response.json(), org_id_ret)
                return retListOfDevices(response.json(), org_id_ret)


def retListOfDevices(json_resp, org_id_ret):
    logger = logging.getLogger("Running retListOfDevices")
    list_of_originId = []
    list_of_orgs = []
    org_origin_list = []
    device_dict = {"ListOfDevice": []}
    for rc in json_resp:
        org_id_devices = {'org_id': rc['org_id'],
                          'devices': []}
        org_origin_json = {'org': rc['org_id'],
                           'list_of_origins': []}
        if rc['originId'] not in org_origin_json['list_of_origins']:
            org_origin_json['list_of_origins'].append(rc['originId'])
            org_origin_list.append(org_origin_json)
        if rc['org_id'] not in list_of_orgs:
            list_of_orgs.append(rc['org_id'])
            data = {'originId': rc['originId'],
                    'device-id': rc['deviceId'],
                    'RC-version': rc['version'],
                    'os-version': rc['osVersion'],
                    'os-name': rc['osVersionName']
                    }
            if data not in org_id_devices['devices']:
                org_id_devices['devices'].append(data)
            device_dict["ListOfDevice"].append(org_id_devices)
            logger.info(f"Returning 'device_per_originId' list.")
        if rc['originId'] not in list_of_originId:
            list_of_originId.append(rc['originId'])
        else:
            data = {'originId': rc['originId'],
                    'device-id': rc['deviceId'],
                    'RC-version': rc['version'],
                    'os-version': rc['osVersion'],
                    'os-name': rc['osVersionName']
                    }
            if org_id_devices['org_id'] == rc['org_id']:
                list_of_orgs.append(rc['org_id'])
                if data not in org_id_devices['devices']:
                    org_id_devices['devices'].append(data)
    # print(f"list_of_originId -> {list_of_originId}")
    # print(f"org_origin_list -> {org_origin_list}")
    return device_dict, org_origin_list


if __name__ == '__main__':
    # Lab API keys
    # API_KEY_ID = "44361325ceb24d9baf001d24bacfa24a"
    # API_KEY = "5de3d86d84fa4a9786039b71d0b4e2c4"
    # # JaleroHome org keys
    # API_KEY_ID = "3a74c8c3bde24c54addffd2f204c6d19"
    # API_KEY = "6bf04ea9b76c475f8c426be08427b739"
    # Lab MSP API creds
    API_KEY_ID = "deae3edd0bcf48059eb072725c3cf5be"
    API_KEY = "f82510d795a34eae8f0f7adf746b82e7"
    fetchRoamingComputers(API_KEY_ID, API_KEY, org_id=8245496)
