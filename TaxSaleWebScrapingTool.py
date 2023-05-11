# Created by: Brad Stricherz
# Created on: May 5th, 2023
# This script imports a CSV file and performs web scraping to check the tax redemption status for each entry in the
# file. The script then deletes any entries that have been redeemed. The script also prints out a list of entries that
# have been redeemed and a list of entries that are likely condos or multiunit properties.

import csv
from bs4 import BeautifulSoup
import requests
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to the database
conn = psycopg2.connect(
    host=os.environ.get('HOST'),
    database=os.environ.get('DATABASE'),
    user=os.environ.get('USER'),
    password=os.environ.get('PASSWORD')
)

valid = []
redeemed = []
condo = []

with open('CitySale216_p9.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # skip the header row
    for row in csv_reader:
        if row[23] != '1116' and row[24] != '1185' and row[24] != '1115':
            url = f'https://dynamic.stlouis-mo.gov/citydata/newdesign/taxinfo.cfm?parcel9={row[94]}'
            html = requests.get(url)
            s = BeautifulSoup(html.content, 'html.parser')
            results = s.findAll('td', string="No")
            if len(results) >= 2:
                valid.append(row[0])
            else:
                redeemed.append(row[0])
        else:
            condo.append(row[0])

print(f"Properties to be deleted: {redeemed}")
print(f"Likely condos or multiunit properties: {condo}")

for i in redeemed:
    cursor = conn.cursor()
    cursor.execute('DELETE FROM "Sale216" WHERE land_id = %s', (i,))
    print(f"Deleted {i}")
    conn.commit()
conn.close()
