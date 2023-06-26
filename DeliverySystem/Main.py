# Author: Stephan Haloftis
# Student ID:

from HashMap import *
from Package import *
from Fleet import *
from Utils import *
from Exceptions import *

import csv
import statistics
import datetime


# Function which populates a HashTable with data from the Package File.
# An improvement to the code would be to have to buildTable function inside the HashMap class
# But the constraints of building the HashMap class per the PA state not to use any libraries or packages
def buildTable(capacity):
    try:
        packagetable = HashMap(capacity)

        workload = Utils.loadPackages()
        workload = csv.reader(workload)
        for packages in workload:
            packageID = int(packages[0])
            address = packages[1]
            city = packages[2]
            state = packages[3]
            zipcode = packages[4]
            deadline = packages[5]
            weight = packages[6]
            note = packages[7]

            package = Package(packageID,
                              address,
                              city,
                              state,
                              zipcode,
                              deadline,
                              weight,
                              Package.Status.HUB.value,
                              note)

            packagetable.add(packageID, package)

        return packagetable
    except csv.Error as e:
        print("Error building table")


# Worst Case: O(n^2)
# deliverPackages function incorporates a variant of the Greedy Algorithm
def deliverPackages(truck):
    # Continues as long as there are packages left to deliver
    while truck.packages:
        distances = []  # Stores the distances from the truck to the packages
        delivered = []
        # Calculates the distance to each package
        for packageID in truck.packages:
            package = hash_table.search(packageID)  # Retrieves the package details
            distance = Utils.findDistance(truck.address,
                                          package.address)  # Calculates the distance from the truck to the package
            if distance is None:
                distance = 0.0
            distances.append((distance, package))  # Appends the distance and package as a tuple to the distances list
        # Finds the package with the smallest distance to the truck
        nearestpackage = min(distances, key=lambda x: x[0])
        # Increases the mileage of the truck by the distance to the nearest package
        truck.mileage += nearestpackage[0]
        # Updates the status of the package to "Delivered"
        nearestpackage[1].status = Package.Status.DEL.value
        # Adds the package to the list of delivered packages
        delivered.append((nearestpackage[1], nearestpackage[1].status))
        # Removes the delivered package from the truck's packages
        truck.packages.remove(nearestpackage[1].ID)
        # Updates the location of the truck to the location of the package that was just delivered
        truck.updateLocation(nearestpackage[1].address)
    # Returns the total mileage of the truck after all packages have been delivered
    return truck.mileage, delivered


# This is an original draft of the algorithm
# The algo always chooses the nearest package to the current address
# The worst-case is O(n^2), mileage is about 204.3 which isn't good enough
# At this point in development I was not keeping track of time
def deliverPackagesOG(truck):
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
deliverPackages(truck1)
deliverPackages(truck2)
deliverPackages(truck3)
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
