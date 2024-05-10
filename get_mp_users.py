import requests
from pprint import pprint
import urllib3

requests.packages.urllib3.disable_warnings() 
urllib3.disable_warnings()

BEARER_TOKEN = "ey..."


def main():
    headers = {
        'authorization': 'Bearer {}'.format(BEARER_TOKEN),
        'content-type': 'application/json',
    }
    json_data = {
        'attributeFilters': {},
        'query': '',
        'pageSize': 10000,
        'principalTypes': [
            'USER',
        ],
    }
    response = requests.post('https://replica.palantirfoundry.com/multipass/api/search/v2/search', headers=headers, json=json_data)

    users = response.json()

    result = []
    for user in users["values"]: 
        cur = {}
        cur["id"] = user["principal"]["id"]
        cur["username"] = user["principal"]["username"]
        if ("userOrg" in user["principal"]["attributes"]): 
            cur["user_org"] = user["principal"]["attributes"]["userOrg"][0]
        else:
            cur["user_org"] = "Unknown"
        result.append(cur)
    pprint(result)
            


main()