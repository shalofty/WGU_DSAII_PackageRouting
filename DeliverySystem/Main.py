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


def generatePath(coordinates):
    origin = [397, 456]  # WGU coordinates
    while len(coordinates) > 0:
        for index, coords in enumerate(coordinates):
            if coords is not None:
                canvas.create_line(origin[0], origin[1], coords[0], coords[1], fill="red", width=3, smooth=True)
                coordinates.pop(index)
                origin = coords


# Worst Case: O(n^2)
# deliverPackages function incorporates a variant of the Greedy Algorithm
def deliverPackages(truck):
    # Continues as long as there are packages left to deliver
    while truck.packages:
        distances = []  # Stores the distances from the truck to the packages
        delivered = []  # Stores the packages that have been delivered
        path = []  # Stores the path that the truck will take
        # Calculates the distance to each package
        for packageID in truck.packages:
            package = hash_table.search(packageID)  # Retrieves the package details
            distance = Utils.findDistance(truck.address, package.address)  # Calculates the distance from the truck to the package
            if distance is None:
                distance = 0.0
            distances.append((distance, package)) # Appends the distance and package as a tuple to the distances list
        # Finds the package with the smallest distance to the truck
        nearestpackage = min(distances, key=lambda x: x[0])
        # Increases the mileage of the truck by the distance to the nearest package
        truck.mileage += nearestpackage[0]
        # Updates the status of the package to "Delivered"
        nearestpackage[1].status = Package.Status.DEL.value
        # Adds the package to the list of delivered packages
        delivered.append((nearestpackage[1], nearestpackage[1].status))
        # Removes the delivered package from the truck's packages
        truck.packages.remove(nearestpackage[1].id)
        # Updates the location of the truck to the location of the package that was just delivered
        truck.updateLocation(nearestpackage[1].address)
    # Returns the total mileage of the truck after all packages have been delivered
    return truck.mileage, delivered, path


hash_table = generateWork(40)
route1 = deliverPackages(truck1)
mileage, delivered, path = route1
print("Total Mileage: ", mileage)
print("Delivered Packages: ", delivered)
print("Path: ", path)
route2 = deliverPackages(truck2)
route3 = deliverPackages(truck3)
totalmileage = truck1.mileage + truck2.mileage + truck3.mileage
print("Total Mileage: ", totalmileage)

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

# establish menuorigin allows for easier menu creation. Typical origin is 0,0
morigin = [672, 756]

root.mainloop()
