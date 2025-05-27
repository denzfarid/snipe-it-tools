import csv

input_file = "files/people-2025-05-27.csv"
output_file = "converted/people-2025-05-27.csv"

snipeit_fields = [
    'First Name', 'Last Name', 'Username', 'Email', 'Phone', 'Address', 'Department',
    'Employee Number', 'Location', 'Notes', 'Job Title', 'Start Date'
]

with open(input_file, newline='', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=snipeit_fields)
    writer.writeheader()

    for row in reader:
        writer.writerow({
            "First Name": row.get("First Name", "").strip(),
            "Last Name": row.get("Last Name", "").strip(),
            "Username": row.get("Email", "").strip(),
            "Email": row.get("Email", "").strip(),
            "Phone": row.get("Phone", "").strip(),
            "Address": row.get("Address", "").strip(),
            "Department": row.get("Departments", "").strip(),
            "Employee Number": row.get("Employee ID", "").strip(),
            "Location": row.get("Locations", "Main Office").strip(),
            "Notes": row.get("Notes", "").strip(),
            "Job Title": row.get("Job Title", "").strip(),
            "Start Date": row.get("Join Date", "").strip()
        })

print(f"Done. Import this file to snipe-it: {output_file}")
