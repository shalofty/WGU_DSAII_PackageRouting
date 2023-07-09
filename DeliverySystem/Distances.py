import csv
from PackageMap import *

map = PackageMap()
addresslist = map.addresslist

def distancetable():
    dt = []
    try:
        with open('distancetable.csv', 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                rowvals = []
                for cell in row[1:]:
                    if cell:
                        rowvals.append(float(cell))
                    else:
                        rowvals.append(float('inf'))
                dt.append(rowvals)
            distancetable = list(dt)
            return distancetable
    except csv.Error as e:
        print(f"Error loading distance table: {e}")


def calculatedistance(currentaddress, destinationaddress):
    currentindex = None
    destinationindex = None
    for address in addresslist:
        if currentaddress == address[2]:
            currentindex = address[0]
            print(currentindex)
        if destinationaddress == address[2]:
            destinationindex = address[0]
            print(destinationindex)
    if currentindex > destinationindex:
        distance = distancetable[currentindex][destinationindex]
        return distance
    elif currentindex < destinationindex:
        distance = distancetable[destinationindex][currentindex]
        return distance
