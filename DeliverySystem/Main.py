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
from tkinter import ttk

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


def generatePath(currentcoordinates, nearestcoordinates, color):
    canvas.create_line(currentcoordinates[0], currentcoordinates[1], nearestcoordinates[0], nearestcoordinates[1], fill=color, width=3, smooth=True, arrow=tk.LAST)


# establish menuorigin allows for easier menu creation. Typical origin is 0,0
morigin = [672, 756]


# Function which populates a HashTable with data from the Package File.
# An improvement to the code would be to have to buildTable function inside the HashMap class
# But the constraints of building the HashMap class per the PA state not to use any libraries or packages
def loadWork():
    capacity = 40
    global packages
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
            # Change the status of the package to 'Processing'
            package.Status = Package.Status.PRO.value
        print("Packages loaded successfully")
        # Return the hash map of packages
        return packages
    except csv.Error as e:  # Catch any csv errors
        # Print an error message if there's a problem with the csv data
        print("Error building table")


# Worst Case: O(n^2)
# deliverPackages function incorporates a variant of the Greedy Algorithm
def deliverPackages(truck, color):
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
            package.coordinates = cords[index]  # Sets the package's address coordinates
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
            truck.updateCoordinates(nearestneighbor[1].coordinates)
        # Add the coordinates of the nearest package to the path with respect to the indexing scheme of the addressfile
        path.append(nearestneighbor[1].coordinates)
        # Finds the coordinates of the nearest package
        nearestcoordinates = Utils.findCoordinates(nearestneighbor[1].address)
        # Draws the path from the truck to the nearest package
        generatePath(currentcoordinates, nearestcoordinates, color)
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
    print(str(truck.name) + " mileage: " + str(truck.mileage))
    return truck.mileage, delivered, path


# Buttons to deliver packages
truck1button = tk.Button(root, text="Truck 1", command=lambda: deliverPackages(truck1, "red"))
truck1button.place(x=morigin[0] + 10, y=morigin[1] - 30)

truck2button = tk.Button(root, text="Truck 2", command=lambda: deliverPackages(truck2, "blue"))
truck2button.place(x=morigin[0] + 10, y=morigin[1] - 60)

truck3button = tk.Button(root, text="Truck 3", command=lambda: deliverPackages(truck3, "green"))
truck3button.place(x=morigin[0] + 10, y=morigin[1] - 90)

# Loads the packages into the hash table data structure
hash_table = loadWork()

# tree = ttk.Treeview(root, columns="Value", show="headings")
#
# tree.heading("Value", text="Value")
#
# tree.column("Value", width=100, anchor="center")
#
# data_list = [1, 2, 3, 4, 5]
#
# for i in data_list:
#     tree.insert("", "end", values=(i,))
#
# tree.place(x=10, y=10)
#
# tree.pack()

tree = ttk.Treeview(root, columns=("Package ID", "Address", "City", "State", "Zip Code", "Deadline", "Weight", "Status", "Note"), show="headings")

tree.heading("Package ID", text="Package ID")

tree.heading("Address", text="Address")

tree.heading("City", text="City")

tree.heading("State", text="State")

tree.heading("Zip Code", text="Zip Code")

tree.heading("Deadline", text="Deadline")

tree.heading("Weight", text="Weight")

tree.heading("Status", text="Status")

tree.heading("Note", text="Note")

tree.column("Package ID", width=100, anchor="center")

tree.column("Address", width=100, anchor="center")

tree.column("City", width=100, anchor="center")

tree.column("State", width=100, anchor="center")

tree.column("Zip Code", width=100, anchor="center")

tree.column("Deadline", width=100, anchor="center")

tree.column("Weight", width=100, anchor="center")

tree.column("Status", width=100, anchor="center")

tree.column("Note", width=100, anchor="center")

data_list = []

for i in range(1, 41):
    package = hash_table.search(i)
    data_list.append((package.id, package.address, package.city, package.state, package.zipcode, package.deadline, package.weight, package.status, package.note))

for i in data_list:
    tree.insert("", "end", values=i)

tree.place(x=10, y=10)

tree.pack()


# Returns the total mileage of all trucks after delivery
def returnTotalMileage():
    if truck1.mileage and truck2.mileage and truck3.mileage is not None:
        totalmileage = round((truck1.mileage + truck2.mileage + truck3.mileage), 2)
        print("Total Mileage: ", totalmileage)
        totalmileagelabel = tk.Label(root, text=f"Total Mileage: {totalmileage}")
        totalmileagelabel.place(x=morigin[0] + 10, y=morigin[1] - 120)
        return totalmileage


totalmileage = returnTotalMileage()

totalmileagebutton = tk.Button(root, text="Total Mileage", command=returnTotalMileage)
totalmileagebutton.place(x=morigin[0] + 10, y=morigin[1] - 150)


root.mainloop()
