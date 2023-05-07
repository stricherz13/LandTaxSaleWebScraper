# Created by: Brad Stricherz
# Created on: May 5th, 2023
# This script will use an imported CSV file and scrapes the web to check tax redemption status.

import csv
from bs4 import BeautifulSoup
import requests

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
            if len(results) > 0:
                valid.append(row[0])
            else:
                redeemed.append(row[0])
        else:
            condo.append(row[0])

print(redeemed)
print(condo)
