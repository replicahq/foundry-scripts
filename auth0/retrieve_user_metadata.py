
import requests
import time
import json
import gzip
import csv


YOUR_DOMAIN = "dev-replica.auth0.com"
YOUR_ACCESS_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJqRTBRa05DTWpKRlJqazBRVFJCTVVJMU1FRkdNelF4T1RCRk9EUTRNVFU1T1VRNU5UQTVSQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1yZXBsaWNhLmF1dGgwLmNvbS8iLCJzdWIiOiJId1BJS3RHRll0akFieUJadUU2SEQ0TmlXOWJxcjlEN0BjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9kZXYtcmVwbGljYS5hdXRoMC5jb20vYXBpL3YyLyIsImlhdCI6MTcwOTA3MTQ2NSwiZXhwIjoxNzA5MTU3ODY1LCJhenAiOiJId1BJS3RHRll0akFieUJadUU2SEQ0TmlXOWJxcjlENyIsInNjb3BlIjoicmVhZDpjbGllbnRfZ3JhbnRzIGNyZWF0ZTpjbGllbnRfZ3JhbnRzIGRlbGV0ZTpjbGllbnRfZ3JhbnRzIHVwZGF0ZTpjbGllbnRfZ3JhbnRzIHJlYWQ6dXNlcnMgdXBkYXRlOnVzZXJzIGRlbGV0ZTp1c2VycyBjcmVhdGU6dXNlcnMgcmVhZDp1c2Vyc19hcHBfbWV0YWRhdGEgdXBkYXRlOnVzZXJzX2FwcF9tZXRhZGF0YSBkZWxldGU6dXNlcnNfYXBwX21ldGFkYXRhIGNyZWF0ZTp1c2Vyc19hcHBfbWV0YWRhdGEgY3JlYXRlOnVzZXJfdGlja2V0cyByZWFkOmNsaWVudHMgdXBkYXRlOmNsaWVudHMgZGVsZXRlOmNsaWVudHMgY3JlYXRlOmNsaWVudHMgcmVhZDpjbGllbnRfa2V5cyB1cGRhdGU6Y2xpZW50X2tleXMgZGVsZXRlOmNsaWVudF9rZXlzIGNyZWF0ZTpjbGllbnRfa2V5cyByZWFkOmNvbm5lY3Rpb25zIHVwZGF0ZTpjb25uZWN0aW9ucyBkZWxldGU6Y29ubmVjdGlvbnMgY3JlYXRlOmNvbm5lY3Rpb25zIHJlYWQ6cmVzb3VyY2Vfc2VydmVycyB1cGRhdGU6cmVzb3VyY2Vfc2VydmVycyBkZWxldGU6cmVzb3VyY2Vfc2VydmVycyBjcmVhdGU6cmVzb3VyY2Vfc2VydmVycyByZWFkOmRldmljZV9jcmVkZW50aWFscyB1cGRhdGU6ZGV2aWNlX2NyZWRlbnRpYWxzIGRlbGV0ZTpkZXZpY2VfY3JlZGVudGlhbHMgY3JlYXRlOmRldmljZV9jcmVkZW50aWFscyByZWFkOnJ1bGVzIHVwZGF0ZTpydWxlcyBkZWxldGU6cnVsZXMgY3JlYXRlOnJ1bGVzIHJlYWQ6cnVsZXNfY29uZmlncyB1cGRhdGU6cnVsZXNfY29uZmlncyBkZWxldGU6cnVsZXNfY29uZmlncyByZWFkOmhvb2tzIHVwZGF0ZTpob29rcyBkZWxldGU6aG9va3MgY3JlYXRlOmhvb2tzIHJlYWQ6ZW1haWxfcHJvdmlkZXIgdXBkYXRlOmVtYWlsX3Byb3ZpZGVyIGRlbGV0ZTplbWFpbF9wcm92aWRlciBjcmVhdGU6ZW1haWxfcHJvdmlkZXIgYmxhY2tsaXN0OnRva2VucyByZWFkOnN0YXRzIHJlYWQ6dGVuYW50X3NldHRpbmdzIHVwZGF0ZTp0ZW5hbnRfc2V0dGluZ3MgcmVhZDpsb2dzIHJlYWQ6c2hpZWxkcyBjcmVhdGU6c2hpZWxkcyBkZWxldGU6c2hpZWxkcyByZWFkOmFub21hbHlfYmxvY2tzIGRlbGV0ZTphbm9tYWx5X2Jsb2NrcyB1cGRhdGU6dHJpZ2dlcnMgcmVhZDp0cmlnZ2VycyByZWFkOmdyYW50cyBkZWxldGU6Z3JhbnRzIHJlYWQ6Z3VhcmRpYW5fZmFjdG9ycyB1cGRhdGU6Z3VhcmRpYW5fZmFjdG9ycyByZWFkOmd1YXJkaWFuX2Vucm9sbG1lbnRzIGRlbGV0ZTpndWFyZGlhbl9lbnJvbGxtZW50cyBjcmVhdGU6Z3VhcmRpYW5fZW5yb2xsbWVudF90aWNrZXRzIHJlYWQ6dXNlcl9pZHBfdG9rZW5zIGNyZWF0ZTpwYXNzd29yZHNfY2hlY2tpbmdfam9iIGRlbGV0ZTpwYXNzd29yZHNfY2hlY2tpbmdfam9iIHJlYWQ6Y3VzdG9tX2RvbWFpbnMgZGVsZXRlOmN1c3RvbV9kb21haW5zIGNyZWF0ZTpjdXN0b21fZG9tYWlucyByZWFkOmVtYWlsX3RlbXBsYXRlcyBjcmVhdGU6ZW1haWxfdGVtcGxhdGVzIHVwZGF0ZTplbWFpbF90ZW1wbGF0ZXMgcmVhZDptZmFfcG9saWNpZXMgdXBkYXRlOm1mYV9wb2xpY2llcyByZWFkOnJvbGVzIGNyZWF0ZTpyb2xlcyBkZWxldGU6cm9sZXMgdXBkYXRlOnJvbGVzIHJlYWQ6cHJvbXB0cyB1cGRhdGU6cHJvbXB0cyByZWFkOmJyYW5kaW5nIHVwZGF0ZTpicmFuZGluZyByZWFkOmxvZ19zdHJlYW1zIGNyZWF0ZTpsb2dfc3RyZWFtcyBkZWxldGU6bG9nX3N0cmVhbXMgdXBkYXRlOmxvZ19zdHJlYW1zIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIn0.k0K4cdL1uOQGEdxXRmiKEqf1l3KMfieyzbzPN792DD2mTkuXNsOkNZn4VuusfMD0gR8h4pN0d6_J0VZGjRX57nqHTiIuYcWTzhPU34vvgA149TPyEybR5rwWZ9vPaB-eP-uYjx73fmab301-2fntsApLtApT3bGQ9JMr73a2FmZ6lTCsWB-4FztdGgUTH4kdeODOEqEetjOlsPvPJj2O_nJGVgbak7XCR24UPVuG9FN6cMMc3_R_WZVzqnNftFmjRkbgAE6iUabEpNYmTjIOSarBMwQKabV-j59YexpOxlX33V4BjX_iMTIp-kZnkb7MOmzs55itm31iDCD3RjzhMw'
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
