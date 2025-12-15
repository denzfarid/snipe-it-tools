import csv
import re
import os

# File input dan output
input_file = 'files/assets-2025-12-10.csv'
output_file = 'converted/assets-2025-12-10.csv'

# Field yang akan ditulis ke file CSV output
snipeit_fields = [
    'Name', 'Asset Tag', 'Serial Number', 'Model', 'Manufacturer', 'Category',
    'Status', 'Location', 'Company', 'Purchase Date', 'Purchase Cost',
    'Order Number', 'Supplier', 'Asset Notes', 'Checked Out to: Username',
    'MAC Address', 'Graphics Card', 'CPU', 'RAM', 'Storage Size',
    'Phone Number', 'IMEI 1', 'IMEI 2', 'Asset Fieldset'
]

# Mapping status Setyl ke Snipe-IT
status_mapping = {
    'in use': 'In Use',
    'storage': 'Storage',
    'stolen': 'Stolen',
    'broken': 'Broken',
    'in repair': 'In Repair'
}

# Keyword pencarian untuk deteksi fieldset
computer_keywords = ['macbook', 'lenovo', 'dell', 'asus', 'hp', 'acer', 'thinkpad', 'elitebook']
phone_keywords = ['iphone', 'samsung', 'poco', 'xiaomi', 'vivo', 'oppo', 'realme', 'infinix']

# Validasi MAC address
def is_valid_mac(mac):
    return bool(re.fullmatch(r'([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}', mac))

# Deteksi fieldset dari nama model
def detect_fieldset(model_name):
    model_name = model_name.lower()
    if any(kw in model_name for kw in computer_keywords):
        return 1  # ID untuk Computer Fields
    elif any(kw in model_name for kw in phone_keywords):
        return 2  # ID untuk Phone Fields
    return ''  # Tidak dikenali

# Pastikan direktori output ada
os.makedirs(os.path.dirname(output_file), exist_ok=True)

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

        model_name = row.get('Model', '').strip()
        fieldset_id = detect_fieldset(model_name)

        status = status_mapping[setyl_status]
        checkout_to = row.get('Assignee', '').strip()

        mac_address = row.get('MAC Address', '').strip()
        if not is_valid_mac(mac_address):
            mac_address = ''

        writer.writerow({
            'Name': row.get('Computer Name', '').strip() or model_name or f"Asset {idx}",
            'Asset Tag': asset_tag,
            'Serial Number': row.get('Serial Number', '').strip(),
            'Model': model_name,
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
            'Storage Size': row.get('Storage Size (GB)', '').strip(),
            'Phone Number': row.get('Phone Number', '').strip(),
            'IMEI 1': row.get('IMEI 1', '').strip(),
            'IMEI 2': row.get('IMEI 2', '').strip(),
            'Asset Fieldset': fieldset_id
        })

print(f"✅ Konversi selesai. File hasil: {output_file}")
