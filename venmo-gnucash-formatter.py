# Creates a nicely-formatted CSV from Venmo statement downloads for import into GnuCash
#
# To run, change to this directory and run: python3 venmo-gnucash-formatter.py

import csv
from datetime import datetime

# Adjust as needed.
inputPath = '/home/jay/Downloads/venmo_statement.csv'
outputPath = '/home/jay/Downloads/venmo_gnucash.csv'


inputFile = open(inputPath)
outputFile = open(outputPath, 'w')

input = csv.DictReader(inputFile)
output = csv.writer(outputFile)
output.writerow(['Date', 'Description', 'Withdrawl', 'Deposit'])

for row in input:
  impactsVenmoBalance = row['Funding Source'] == 'Venmo balance' or row['Destination'] == 'Venmo balance'

  if impactsVenmoBalance :
    date = datetime.fromisoformat(row['Datetime']).date().isoformat()

    description = row['Note']

    amountStr = row['Amount (total)']
    withdrawl = ''
    deposit = ''
    if amountStr.startswith('-'):
      withdrawl = amountStr[1:]
    else:
      deposit = amountStr

    output.writerow([date, description, withdrawl, deposit])
  

