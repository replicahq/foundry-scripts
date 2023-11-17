import requests
from pprint import pprint
import urllib3
urllib3.disable_warnings()

BEARER_TOKEN = "ey"

MAGRITTE_SOURCE = 'ri.magritte..source.04421156-f95a-4d1f-b1df-a55f43ce3b11'  # rid for relevant magritte source
PARENT_COMPASS_FOLDER_RID = "ri.compass.main.folder.b21c94c4-c8a5-4001-b806-faaeff4bc0c4"  # rid for relevant compass folder
MARKINGS = []

TABLES = [
	# BQ table name 1
]

def create_dataset(table):

	headers = {
	    'authorization': 'Bearer {}'.format(TOKEN),
	    'content-type': 'application/json',
	}

	json= {
	    'requestWithName': {
	        'name': table,
	        'parentRid': PARENT_COMPASS_FOLDER_RID,
	        'markings': MARKINGS,
	    },
	    'type': 'requestWithName',
	}

	response = requests.post(
	    'https://replica.palantirfoundry.com/foundry-catalog/api/catalog/createDataset2',
	    headers=headers,
	    json=json,
	)
	if response.status_code in [200, 204]:
		print("SUCCESS: Created dataset: {}".format(response.json()["rid"]))
	else:
		print ("FAILED TO CREATE DATASET")
	return response.json()

def create_sync(dataset_rid, project, folder, table):

	headers = {
	    'authorization': 'Bearer {}'.format(TOKEN),
	    'content-type': 'application/json',
	}

	params = {
	    'branchName': 'master',
	}

	json_data = {
	    'sourceId': MAGRITTE_SOURCE,
	    'extractName': table,
	    'datasetId': dataset_rid,
	    'extractConfig': {
	        'sourceAdapter': {
	            'type': 'bigquery',
	            'config': {
	                'api': {
	                    'storageRead': {
	                        'table': {
	                            'project': project,
	                            'dataset': folder,
	                            'table': table
	                        },
	                    },
	                    'type': 'storageRead',
	                },
	            },
	        },
	        'outputOptions': {
	            'transactionType': 'SNAPSHOT',
	            'outputConstraints': [
	                {
	                    'consistentOutputSchema': {},
	                    'type': 'consistentOutputSchema',
	                },
	            ],
	        },
	    },
	    'branchName': 'master',
	    'sparkProfiles': [],
	}

	response = requests.post(
	    'https://replica.palantirfoundry.com/magritte-coordinator/api/build/add-extract',
	    params=params,
	    headers=headers,
	    json=json_data,
	)	
	if response.status_code in [200, 204]:
		print("SUCCESS: Created Sync")
	else:
		print ("FAILED TO CREATE SYNC")
	pass


def main():
	for location in TABLES:
		project, folder, table = location.split(".")
		print("\n\n TABLE: {}".format(location))
		dataset = create_dataset(table)
		create_sync(dataset["rid"], project, folder, table)
		# return

main()
