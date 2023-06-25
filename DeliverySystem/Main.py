# Author: Stephan Haloftis
# Student ID:

from HashMap import *
from Package import *
from Fleet import *
from Utils import *

import csv
import datetime


# Function which populates a HashTable with data from the Package File.
# An improvement to the code would be to have to buildTable function inside the HashMap class
# But the constraints of building the HashMap class per the PA state not to use any libraries or packages
def buildTable(capacity):
    try:
        packagetable = HashMap(capacity)

        packagefile = Utils.loadPackages()
        packagefile = csv.reader(packagefile)
        for row in packagefile:
            packageID = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zipcode = row[4]
            deadline = row[5]
            weight = row[6]

            package = Package(packageID,
                              address,
                              city,
                              state,
                              zipcode,
                              deadline,
                              weight,
                              Package.Status.HUB.value)

            packagetable.add(packageID, package)

        return packagetable
    except csv.Error as e:
        print("Error building table")


def deliverPackages(truck):
    preshipment = []
    try:
        for packageID in truck.packages:
            package = hash_table.search(packageID)
            preshipment.append(package)
        truck.packages.clear()
        currentAddress = Utils.getAddress(truck.address)

        while preshipment:
            shortestDistance = float('inf')
            nextPackage = None

            for package in preshipment:
                packageAddress = Utils.getAddress(package.address)
                distance = Utils.findDistance(currentAddress, packageAddress)

                if distance <= shortestDistance:
                    shortestDistance = distance
                    nextPackage = package

            truck.packages.append(nextPackage.ID)
            preshipment.remove(nextPackage)
            truck.mileage += shortestDistance
            truck.address = nextPackage.address

    except csv.Error as e:
        print("Error delivering packages")

hash_table = buildTable(40)
deliverPackages(truck1)
deliverPackages(truck2)
print(truck1.packages)
print(truck2.packages)

# Test Code
# hash_table = buildTable(40)
# i = 1
# while i <= 40:
#     value = hash_table.search(i)
#     print(value)
#     i += 1
