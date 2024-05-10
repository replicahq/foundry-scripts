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
    data = '{"cacheToken":"","query":""}'
    
    response = requests.post(
        'https://replica.palantirfoundry.com/multipass/api/internal/principal/groups',
        headers=headers,
        data=data,
    )
    groups = [[x["group"]["name"], x["group"]["id"]] for x in response.json()["rows"]]
    print("name|id")
    for x in groups: 
        print(f"{x[0]}|{x[1]}")




main()
