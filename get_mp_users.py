import requests
from pprint import pprint
import urllib3

requests.packages.urllib3.disable_warnings() 
urllib3.disable_warnings()

BEARER_TOKEN = ""


def main():
    headers = {
        'authorization': 'Bearer {}'.format(BEARER_TOKEN),
        'content-type': 'application/json',
    }
    json_data = {
        'attributeFilters': {},
        'query': '',
        'pageSize': 1000,
        'principalTypes': [
            'USER',
        ],
    }
    response = requests.post('https://replica.palantirfoundry.com/multipass/api/search/v2/search', headers=headers, json=json_data)

    users = response.json()
    users = [{
        "id": x["principal"]["id"],
        "username": x["principal"]["username"],
    }for x in users["values"]]

    for x in users:
        print("{},{}".format(x["id"], x["username"]))


main()