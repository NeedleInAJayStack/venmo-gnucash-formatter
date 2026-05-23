#! /usr/bin/python3

# Creates a nicely-formatted CSV from Venmo statement downloads for import into GnuCash
#
# To run (change to this directory):
# python3 venmo-gnucash-formatter.py -d ~/Downloads

import argparse
import csv
from datetime import datetime

all_args = argparse.ArgumentParser()
all_args.add_argument("-f", "--file", required=True,
   help="The path of the input csv file.")
all_args.add_argument("-o", "--output", required=True,
   help="The path of the output csv file.")
args = vars(all_args.parse_args())

inputPath = str(args["file"])
outputPath = str(args["output"])


inputFile = open(inputPath)
outputFile = open(outputPath, 'w')

next(inputFile)  # Skip "Account Statement" line
next(inputFile)  # Skip "Account Activity" line
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
    if amountStr.startswith('- $'):
      withdrawl = amountStr[3:]
    elif amountStr.startswith('-$'):
      withdrawl = amountStr[2:]
    elif amountStr.startswith('-'):
      withdrawl = amountStr[1:]
    elif amountStr.startswith('+ $'):
      deposit = amountStr[3:]
    elif amountStr.startswith('$'):
      deposit = amountStr[1:]
    else:
      deposit = amountStr

    output.writerow([date, description, withdrawl, deposit])
  

