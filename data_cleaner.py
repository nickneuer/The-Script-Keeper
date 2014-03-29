
import sys
import csv

def clean_row(row):
  if row:
    RTD = row[10]
    YTD = row[9]
    TW = row[8] 
    price = row[4]     
    row[4],row[8],row[9],row[10] = "".join(price.split("$")), "".join(TW.split(",")), "".join(YTD.split(",")), "".join(RTD.split(",")) 

with open(sys.argv[1], 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  rows = []
  for row in reader:
    if row:
      rows.append(row)



map(clean_row, rows)

with open(sys.argv[2], 'wb') as outfile:
  writer = csv.writer(outfile, delimiter=';')
  writer.writerows(rows)

