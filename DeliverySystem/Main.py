# Author: Stephan Haloftis
# Student ID: 010727171

from HashMap import *
from Package import *
from Fleet import *
from Utils import *
from Exceptions import *
from Coords import coordinates

import csv
import datetime
import tkinter as tk

### GUI Code ###
root = tk.Tk()
root.title("Package Delivery System")

# Load the map image
map = tk.PhotoImage(file="map.png")
w = map.width()
h = map.height()
# Create a canvas that can fit the above image
canvas = tk.Canvas(root, width=(w + 200), height=h, bg="white")
canvas.pack(expand=tk.YES, fill=tk.BOTH)
canvas.create_image(0, 0, image=map, anchor=tk.NW)


def generatePath(currentcoordinates, nearestcoordinates):
    canvas.create_line(currentcoordinates[0], currentcoordinates[1], nearestcoordinates[0], nearestcoordinates[1], fill="blue", width=3, smooth=True, arrow=tk.LAST)


# establish menuorigin allows for easier menu creation. Typical origin is 0,0
morigin = [672, 756]


# Function which populates a HashTable with data from the Package File.
# An improvement to the code would be to have to buildTable function inside the HashMap class
# But the constraints of building the HashMap class per the PA state not to use any libraries or packages
def generateWork(capacity):
    try:
        # Create a hash map with a size of 'capacity'
        packages = HashMap(capacity)
        # Load the package data using the loadPackages utility
        workload = Utils.loadPackages()
        # Convert the package data into a csv reader object
        workload = csv.reader(workload)
        # Iterate over each row in the csv reader
        for objects in workload:
            # Extract the package information from the row
            packageID = int(objects[0])
            address = objects[1]
            city = objects[2]
            state = objects[3]
            zipcode = objects[4]
            deadline = objects[5]
            weight = objects[6]
            note = objects[7]
            # Create a new Package object with the extracted data
            package = Package(packageID,
                              address,
                              city,
                              state,
                              zipcode,
                              deadline,
                              weight,
                              Package.Status.HUB.value,
                              note)
            # Add the new Package to the hash map using the packageID as the key
            packages.add(packageID, package)
            # Change the status of the package to 'Out for Delivery'
            package.Status = Package.Status.OUT.value
        # Return the hash map of packages
        return packages
    except csv.Error as e:  # Catch any csv errors
        # Print an error message if there's a problem with the csv data
        print("Error building table")


# Worst Case: O(n^2)
# deliverPackages function incorporates a variant of the Greedy Algorithm
def deliverPackages(truck):
    # Continues as long as there are packages left to deliver
    while truck.packages:
        cords = []
        packages = []  # Stores the packages that are to be delivered
        distances = []  # Stores the distances from the truck to the packages
        delivered = []  # Stores the packages that have been delivered
        path = []  # Stores the path that the truck will take
        # Append coordinates to cords array
        for xy in coordinates:
            cords.append(xy)
        # Add distances and packages to the distances and packages lists
        for index, packageID in enumerate(truck.packages):
            package = hash_table.search(packageID)  # Retrieves the package details
            package.acoords = cords[index]  # Sets the package's address coordinates
            distance = Utils.findDistance(truck.address, package.address)  # Calculates the distance from the truck to the package
            if distance is None:
                distance = 0.0
            # Adds the distance and package to the distances list
            distances.append((distance, package))
            # Add the package to the packages list
            packages.append(package)
        # Finds the package with the smallest distance to the truck
        nearestneighbor = min(distances, key=lambda x: x[0])
        # Save current truck coordinates
        currentcoordinates = truck.coordinates
        # Update truck coordinates to nearest package coordinates
        if truck.address == "4001 South 700 East":  # Hub address
            truck.updateLocation(nearestneighbor[1].address)
            truck.updateCoordinates(nearestneighbor[1].acoords)
        # Add the coordinates of the nearest package to the path with respect to the indexing scheme of the addressfile
        path.append(nearestneighbor[1].acoords)
        # Finds the coordinates of the nearest package
        nearestcoordinates = Utils.findCoordinates(nearestneighbor[1].address)
        # Draws the path from the truck to the nearest package
        generatePath(currentcoordinates, nearestcoordinates)
        # Increases the mileage of the truck by the distance to the nearest package
        truck.mileage += nearestneighbor[0]
        # Updates the location of the truck to the location of the package that was just delivered
        truck.updateLocation(nearestneighbor[1].address)
        # Updates the coordinates of the truck to the coordinates of the package that was just delivered
        truck.updateCoordinates(nearestcoordinates)
        # Updates the status of the package to "Delivered"
        nearestneighbor[1].status = Package.Status.DEL.value
        # Adds the package to the list of delivered packages
        delivered.append((nearestneighbor[1], nearestneighbor[1].status))
        # Removes the delivered package from the truck's packages
        truck.packages.remove(nearestneighbor[1].id)


    # Returns the total mileage of the truck after all packages have been delivered
    return truck.mileage, delivered, path


hash_table = generateWork(40)
route1 = deliverPackages(truck1)
# mileage, delivered, path = route1
# print("Total Mileage: ", mileage)
# print("Delivered Packages: ", delivered)
# print("Path: ", path)
# route2 = deliverPackages(truck2)
# route3 = deliverPackages(truck3)
totalmileage = truck1.mileage + truck2.mileage + truck3.mileage
print("Total Mileage: ", totalmileage)

root.mainloop()
