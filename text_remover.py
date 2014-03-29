import csv
import sys

top = "\nTitle Lookup\nSearch By\tOptions\tSearch For\t\n\t\t\t\nAuthor \tTitle \tISBN-13 \tBinding \tPrice \tBisac \tPublisher \tPublish\nDate \tTW\nSales \tYTD\nSales \tRTD\nSales"

bottom = "\nCopyright \xc2\xa9 2014 Nielsen BookScan, a division of Nielsen Entertainment, LLC. All rights reserved.\n"

with open(sys.argv[1]) as file:
  text = file.read().replace(top, "").replace(bottom, "")
  rows = text.split("\n")
  values = []
  for row in rows:
    if row:
      values.append(row.split("\t"))
      
   
with open(sys.argv[2], "wb") as file:
  writer = csv.writer(file, delimiter = "\t") 
  writer.writerows(values)








