import requests


# Test function
def createNtwDevice():

    url = "https://api.umbrella.com/deployments/v2/networkdevices"

    payload = '''{
        "model": "ModelName",
        "macAddress": "0123456789ab",
        "name": "label1",
        "serialNumber": "12345a"
    }'''

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.request('POST', url, headers=headers, data = payload)

    print(response.text.encode('utf8'))
