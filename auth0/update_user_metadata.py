import requests
import csv
from pprint import pprint
import psycopg2
from metastore_config import load_config


AUTH0_DOMAIN = "dev-replica.auth0.com"
AUTH0_BEARER_TOKEN = 'ey...'
USER_CSV = 'auth0_users_with_metadata_check.csv'

def get_users_to_update(csv_path): 
    with open(csv_path, mode='r') as infile:
        reader = csv.DictReader(infile)
        return [row for row in reader if row["has_user_metadata"] == "0"]
    
def query_org_info(user, metastore_config):
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**metastore_config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    pass

def write_org_info(org_id, org_name):
    pass

def main():
    users = get_users_to_update(USER_CSV)

    metastore_config = load_config()
    for user in users: 
        query_org_info(user, metastore_config)
        # write_org_info(org_id, org_name)

        return
        
main()