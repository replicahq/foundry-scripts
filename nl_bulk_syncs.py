import requests
from pprint import pprint
import urllib3

urllib3.disable_warnings()

BEARER_TOKEN = ""

MAGRITTE_SOURCE = "ri.magritte..source.514ae5ce-56d4-48cf-b285-6c1c33b81a68"  # rid for relevant magritte source
PARENT_COMPASS_FOLDER_RID = "ri.compass.main.folder.703b31db-4acd-4c2d-807c-368252b22674"  # rid for relevant compass folder
MARKINGS = []

REGIONS = [
    # "alaska",
    "cal_nev",
    "great_lakes",
    "hawaii",
    "mid_atlantic",
    "north_atlantic",
    "north_central",
    "northeast",
    "northwest",
    "south_atlantic",
    "south_central",
    "southwest",
]
# DAYS = ["thursday", "saturday"]
# SEASONS = ["2019_Q4", "2021_Q2", "2021_Q4", "2022_Q4", "2023_Q2"]
DAYS = ["thurs"]
SEASONS = ["2023_q2"]


def generate_table_names():
    tables = []
    for region in REGIONS:
        for season in SEASONS:
            for day in DAYS:
                tables.append(
                    "core-data-service-prod.nl_breakdown.{}_{}_{}".format(
                        region, season, day
                    )
                )
    return tables


def create_dataset(table):
    headers = {
        "authorization": "Bearer {}".format(BEARER_TOKEN),
        "content-type": "application/json",
    }

    json = {
        "requestWithName": {
            "name": table,
            "parentRid": PARENT_COMPASS_FOLDER_RID,
            "markings": MARKINGS,
        },
        "type": "requestWithName",
    }

    response = requests.post(
        "https://replica.palantirfoundry.com/foundry-catalog/api/catalog/createDataset2",
        headers=headers,
        json=json,
    )
    if response.status_code in [200, 204]:
        print("SUCCESS: Created dataset: {}".format(response.json()["rid"]))
    else:
        print("FAILED TO CREATE DATASET")
    return response.json()


def create_sync(dataset_rid, project, folder, table):
    headers = {
        "authorization": "Bearer {}".format(BEARER_TOKEN),
        "content-type": "application/json",
    }

    params = {
        "branchName": "master",
    }

    json_data = {
        "sourceId": MAGRITTE_SOURCE,
        "extractName": table,
        "datasetId": dataset_rid,
        "extractConfig": {
            "sourceAdapter": {
                "type": "bigquery",
                "config": {
                    "api": {
                        "storageRead": {
                            "table": {
                                "project": project,
                                "dataset": folder,
                                "table": table,
                            },
                        },
                        "type": "storageRead",
                    },
                },
            },
            "outputOptions": {
                "transactionType": "SNAPSHOT",
                "outputConstraints": [
                    {
                        "consistentOutputSchema": {},
                        "type": "consistentOutputSchema",
                    },
                ],
            },
        },
        "branchName": "master",
        "sparkProfiles": [],
    }

    response = requests.post(
        "https://replica.palantirfoundry.com/magritte-coordinator/api/build/add-extract",
        params=params,
        headers=headers,
        json=json_data,
    )
    if response.status_code in [200, 204]:
        print("SUCCESS: Created Sync")
    else:
        print("FAILED TO CREATE SYNC")
    pass


def main():
    tables = generate_table_names()
    print(tables)
    for location in tables:
        # print("hello")
        project, folder, table = location.split(".")
        print("\n\n TABLE: {}".format(location))
        dataset = create_dataset(table)
        create_sync(dataset["rid"], project, folder, table)
    # return


main()
