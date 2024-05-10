
import requests
import time
import json
import gzip
import csv


YOUR_DOMAIN = "dev-replica.auth0.com"
YOUR_ACCESS_TOKEN = 'ey...'
gzip_file_path = 'auth0_users_export.jsonl.gz'
output_csv_path = 'auth0_users_with_metadata_check.csv'


def start_export_job(domain, token):
    url = f"https://{domain}/api/v2/jobs/users-exports"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "format": "json",
        "fields": [
            {"name": "user_id"},
            {"name": "email"},
            {"name": "created_at"},
            {"name": "user_metadata"}
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["id"]
    else:
        print(f"Error starting export job: {response.status_code} - {response.text}")
        return None

def check_job_status(domain, token, job_id):
    url = f"https://{domain}/api/v2/jobs/{job_id}"
    headers = {"Authorization": f"Bearer {token}"}
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            job = response.json()
            if job["status"] == "completed":
                return job["location"]
            elif job["status"] in ["pending", "processing"]:
                print("Job is still processing. Waiting...")
                time.sleep(10)
            else:
                print(f"Job failed with status: {job['status']}")
                return None
        else:
            print(f"Error checking job status: {response.status_code}")
            return None

def download_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"File downloaded: {filename}")
    else:
        print(f"Error downloading file: {response.status_code}")


def decompress_jsonl_and_write_csv(gzip_file_path, output_csv_path):
    with gzip.open(gzip_file_path, 'rt', encoding='utf-8') as gz_file:
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['user_id', 'email', 'created_at', 'has_user_metadata']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for line in gz_file:
                user = json.loads(line)
                writer.writerow({
                    'user_id': user.get('user_id', ''),
                    'email': user.get('email', ''),
                    'created_at': user.get('created_at', ''),
                    'has_user_metadata': 0 if not user.get('user_metadata') else 1
                })


job_id = start_export_job(YOUR_DOMAIN, YOUR_ACCESS_TOKEN)

if job_id:
    print(f"Export job started with ID: {job_id}")

    file_url = check_job_status(YOUR_DOMAIN, YOUR_ACCESS_TOKEN, job_id)
    if file_url:
        download_file(file_url, gzip_file_path)

decompress_jsonl_and_write_csv(gzip_file_path, output_csv_path)

print(f"CSV file has been created at {output_csv_path}.")
