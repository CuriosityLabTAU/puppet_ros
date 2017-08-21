
import csv

f = open('export_3.csv')
csv_f = csv.reader(f)

mouth = []

map = 150.0/255
print map
for row in csv_f:
    a = float(row[0])*map
    mouth.append(a)

print mouth