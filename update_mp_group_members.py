import requests
from pprint import pprint
import urllib3

requests.packages.urllib3.disable_warnings() 
urllib3.disable_warnings()

BEARER_TOKEN = "ey ... "
HEADERS = {
        'authorization': 'Bearer {}'.format(BEARER_TOKEN),
        'content-type': 'application/json',
    }

GROUP_ID = '8761c53c-5bbf-4932-a9db-450c5df485ff'
UPDATED_MEMBER_PRINCIPLE_IDS = [
    '51aaabe5-5171-463a-870d-133c7c2c41b0'
]

def get_group_members(group_id: str, headers:dict[str,str]=HEADERS): 
    url = f'https://replica.palantirfoundry.com/multipass/api/administration/groups/{group_id}/members'
    response = requests.get(
        url,
        headers=headers,
    )
    if response.status_code in [200, 204]:
        print("Successfully fetched members of group with id: {}".format(group_id))
    else:
        raise ValueError(response.text)
    return response.json()

def add_principles_to_group(group_id: str, principle_ids: list[str], headers:dict[str,str]=HEADERS):
    url = 'https://replica.palantirfoundry.com/multipass/api/administration/groups/bulk/members'
    json_data = {
        'groupIds': [
            group_id,
        ],
        'principalIds': principle_ids,
        'expirations': {
            '8761c53c-5bbf-4932-a9db-450c5df485ff': {},
        },
    }

    response = requests.post(
        url,
        headers=headers,
        json=json_data,
    )
    if response.status_code in [200, 204]:
        print("Successfully added new members to group with id: {}".format(group_id))
    else:
        raise ValueError(response.text)

def remove_group_members(group_id: str, to_remove: list[str], headers:dict[str,str]=HEADERS):
    url = f"https://replica.palantirfoundry.com/multipass/api/administration/groups/{group_id}/members"

    response = requests.delete(
        url,
        headers=headers,
        json=to_remove,
    )
    if response.status_code in [200, 204]:
        print("Successfully removed excess members from group with id: {}".format(group_id))
    else:
        raise ValueError(response.text)

def main():
    existing_members = get_group_members(GROUP_ID)
    existing_members = [x["id"] for x in existing_members]
    print("existing Members: ", existing_members)
    add_principles_to_group(GROUP_ID, UPDATED_MEMBER_PRINCIPLE_IDS)

    to_remove = [x for x in existing_members if x not in UPDATED_MEMBER_PRINCIPLE_IDS]
    print ("removing groups: ", to_remove)
    remove_group_members(GROUP_ID, to_remove)

main()
