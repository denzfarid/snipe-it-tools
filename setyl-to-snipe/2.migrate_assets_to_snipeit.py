import csv
import re

# File input dan output
input_file = 'files/assets-2025-05-27.csv'
output_file = 'converted/assets-2025-05-27.csv'

snipeit_fields = [
    'Name', 'Asset Tag', 'Serial Number', 'Model', 'Manufacturer', 'Category',
    'Status', 'Location', 'Company', 'Purchase Date', 'Purchase Cost',
    'Order Number', 'Supplier', 'Asset Notes', 'Checked Out to: Username',
    'MAC Address', 'Graphics Card', 'CPU', 'RAM', 'Storage Size',
    'Phone Number', 'IMEI 1', 'IMEI 2'
]

# Mapping status Setyl ke Snipe-IT
status_mapping = {
    'in use': 'In Use',
    'storage': 'Storage',
    'stolen': 'Stolen',
    'broken': 'Broken',
    'in repair': 'In Repair'
}

# Validasi MAC address
def is_valid_mac(mac):
    return bool(re.fullmatch(r'([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}', mac))

with open(input_file, newline='', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=snipeit_fields)
    writer.writeheader()

    for idx, row in enumerate(reader, start=1):
        setyl_status = row.get('Status', '').strip().lower()

        # Hanya proses jika status cocok dengan mapping
        if setyl_status not in status_mapping:
            continue

        asset_tag = row.get('Asset ID', '').strip()
        if not asset_tag:
            asset_tag = f"AUTO-{str(idx).zfill(4)}"

        status = status_mapping[setyl_status]
        checkout_to = row.get('Assignee', '').strip()

        mac_address = row.get('MAC Address', '').strip()
        if not is_valid_mac(mac_address):
            mac_address = ''

        writer.writerow({
            'Name': row.get('Model', '').strip() or f"Asset {idx}",
            'Asset Tag': asset_tag,
            'Serial Number': row.get('Serial Number', '').strip(),
            'Model': row.get('Model', '').strip(),
            'Manufacturer': row.get('Manufacturer', '').strip(),
            'Category': row.get('Type', '').strip(),
            'Status': status,
            'Location': row.get('Locations', 'Main Office').strip(),
            'Company': row.get('Legal Entities', 'PT ITSEC ASIA Tbk').strip() or 'PT ITSEC ASIA Tbk',
            'Purchase Date': row.get('Purchased on', '').strip(),
            'Purchase Cost': row.get('Price', '').strip(),
            'Order Number': row.get('Purchase Order No.', '').strip(),
            'Supplier': row.get('Supplier Name', '').strip(),
            'Asset Notes': row.get('Notes', '').strip(),
            'Checked Out to: Username': checkout_to,
            'MAC Address': mac_address,
            'Graphics Card': row.get('Graphics Card', '').strip(),
            'CPU': row.get('CPU', '').strip(),
            'RAM': row.get('RAM', '').strip(),
            'Storage Size': row.get('Storage Size', '').strip(),
            'Phone Number': row.get('Phone Number', '').strip(),
            'IMEI 1': row.get('IMEI 1', '').strip(),
            'IMEI 2': row.get('IMEI 2', '').strip()
        })

print(f"Done. Import this file to snipe-it: {output_file}")
