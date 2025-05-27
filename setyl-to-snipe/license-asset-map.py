import requests
import csv
import time
import urllib3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SNIPEIT_URL = "https://example.com/api/v1"
API_TOKEN = "Bearer <PASTE TOKEN HERE>"

HEADERS = {
    "Authorization": API_TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json"
}
CSV_FILE = 'files/license-windows-map.csv'

session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    raise_on_status=False
)
adapter = HTTPAdapter(max_retries=retries)
session.mount('https://', adapter)
session.mount('http://', adapter)

def get_license_id_by_product_key(product_key):
    url = f"{SNIPEIT_URL}/licenses?search={product_key}"
    response = session.get(url, headers=HEADERS, verify=False)
    if response.status_code == 200:
        results = response.json().get('rows', [])
        for lic in results:
            if lic.get('product_key') == product_key:
                return lic['id']
    return None

def get_asset_id_by_tag(asset_tag):
    url = f"{SNIPEIT_URL}/hardware?search={asset_tag}"
    response = session.get(url, headers=HEADERS, verify=False)
    if response.status_code == 200:
        results = response.json().get('rows', [])
        for asset in results:
            if asset.get('asset_tag') == asset_tag:
                return asset['id']
    return None

def get_available_seat_id(license_id):
    url = f"{SNIPEIT_URL}/licenses/{license_id}/seats"
    response = session.get(url, headers=HEADERS, verify=False)
    if response.status_code == 200:
        data = response.json()
        for seat in data.get("rows", []):
            if not seat.get("assigned_user") and not seat.get("assigned_asset"):
                return seat["id"]
    return None

def assign_seat_to_asset(license_id, seat_id, asset_id):
    url = f"{SNIPEIT_URL}/licenses/{license_id}/seats/{seat_id}"
    payload = {
        "asset_id": asset_id
    }
    response = session.put(url, headers=HEADERS, json=payload, verify=False)
    if response.status_code == 200:
        return True
    else:
        print(f"[ERROR] Failed to assign seat_id {seat_id} to asset_id {asset_id}: {response.status_code} - {response.text}")
        return False

# MAIN PROCESS
with open(CSV_FILE, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        asset_tag = row.get('Asset Tag', '').strip()
        product_key = row.get('Product Key', '').strip()

        if not asset_tag or not product_key:
            print(f"[WARNING] Skipping blank or invalid lines: {row}")
            continue

        print(f"[INFO] Process: Asset Tag: {asset_tag}, Product Key: {product_key}")

        license_id = get_license_id_by_product_key(product_key)
        if not license_id:
            print(f"[ERROR] License for product key '{product_key}' not found.")
            continue

        asset_id = get_asset_id_by_tag(asset_tag)
        if not asset_id:
            print(f"[ERROR] Asset with tag '{asset_tag}' not found.")
            continue

        seat_id = get_available_seat_id(license_id)
        if not seat_id:
            print(f"[ERROR] No seats available for license ID {license_id}")
            continue

        if assign_seat_to_asset(license_id, seat_id, asset_id):
            print(f"[SUCCESS] Seat {seat_id} for license '{product_key}' successfully assigned to asset '{asset_tag}'")
        else:
            print(f"[FAIL] Failed to assign seat license '{product_key}' to asset '{asset_tag}'")

        time.sleep(1)
