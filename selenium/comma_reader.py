import csv
with open('/home/ehab/Book1.csv', 'rb') as csvfile:
    myrows = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in myrows:
        print (row[1])