import csv

input_file = "files/windows-pro.txt"
output_file = "converted/windows-pro.csv"

# Template Column Snipe-IT License
# "Seats": 1 Total available seat
license_template = {
    "Name": "Windows Pro",
    "Product Key": "",
    "Expiration Date": "",
    "Licensed to Email": "",
    "Licensed to Name": "",
    "Manufacturer": "Microsoft",
    "Min. QTY": "0",
    "Seats": 1,
    "Category": "Misc Software"
}

with open(input_file, "r", encoding="utf-8") as infile, \
     open(output_file, "w", newline='', encoding="utf-8") as outfile:

    writer = csv.DictWriter(outfile, fieldnames=license_template.keys())
    writer.writeheader()

    for line in infile:
        product_key = line.strip()
        if product_key:
            license_data = license_template.copy()
            license_data["Product Key"] = product_key
            writer.writerow(license_data)

print(f"Done. Import this file to snipe-it: {output_file}")
