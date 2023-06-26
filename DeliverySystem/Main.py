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


# def deliverPackages(truck):
#     preshipment = []
#     try:
#         for packageID in truck.packages:
#             package = hash_table.search(packageID)
#             preshipment.append(package)
#         truck.packages.clear()
#         currentaddress = Utils.getAddress(truck.address)
#
#         while preshipment:
#             shortestDistance = float('inf')
#             nextPackage = None
#
#             for package in preshipment:
#                 packageaddress = Utils.getAddress(package.address)
#                 distance = Utils.findDistance(currentaddress, packageaddress)
#
#                 if distance <= shortestDistance:
#                     shortestDistance = distance
#                     nextPackage = package
#
#             truck.packages.append(nextPackage.ID)
#             preshipment.remove(nextPackage)
#             truck.mileage += shortestDistance
#             truck.address = nextPackage.address
#
#     except csv.Error as e:
#         print("Error delivering packages")


# def deliverLoad(truck):
#     load = []
#     distances = []
#     try:
#         for packageid in truck.packages:
#             package = hash_table.search(packageid)
#             distance = Utils.findDistance(truck.address, package.address)
#             load.append(package)
#             distances.append(distance)
#             hash_table.hash_remove(packageid)
#             nearest = min(distances)
#             index = distances.index(nearest)
#             # nearestaddress = addresses[index]
#             print("Number of packages in truck: ", len(truck.packages))
#             if len(truck.packages) == 0:
#                 truck.mileage += sum(distances)
#                 print(truck.mileage)
#                 break
#
#         truck.packages.clear()
#     except csv.Error as e:
#         print("Error delivering packages")


# Currently incorporating a greedy algorithm to deliver packages
# The algo always chooses the nearest package to the current address
def deliver(truck):
    packages = []
    distances = []
    path = []
    outfordelivery = True
    index = 0
    unprocessed = True
    currentaddress = truck.address
    while outfordelivery:
        if unprocessed:
            # Assign package to variable
            package = hash_table.search(truck.packages[index])
            # Calculate distance from current address to package address
            distance = Utils.findDistance(currentaddress, package.address)
            # Add package to list of packages
            packages.append(package)
            # Add distance to list of distances
            distances.append(distance)
            # Update truck location to package address which prepares for next iteration
            truck.updateLocation(package.address)
            # Remove package from hash table
            hash_table.hash_remove(package.ID)
            # Increment delivery index
            index += 1
        # If incremented through all packages in truck
        if index == (len(truck.packages)):
            unprocessed = False  # Disables first if statement
            # Find nearest package
            nearest = min(distances)
            # Find index of nearest package
            nindex = distances.index(nearest)
            # Add nearest package to path
            path.append(distances[nindex])
            # Remove nearest package from packages list
            distances.pop(nindex)
            truck.mileage += nearest
        if len(distances) == 0:
            outfordelivery = False
            print("Truck Mileage: ", truck.mileage)
            return truck.mileage


hash_table = buildTable(40)

deliver(truck1)
deliver(truck2)
deliver(truck3)
totalmileage = truck1.mileage + truck2.mileage + truck3.mileage
print("Total Mileage: ", totalmileage)
# Working on getting it below 140 miles, currently at 204.3 miles

# Test Code
# hash_table = buildTable(40)
# i = 1
# while i <= 40:
#     value = hash_table.search(i)
#     print(value)
#     i += 1
