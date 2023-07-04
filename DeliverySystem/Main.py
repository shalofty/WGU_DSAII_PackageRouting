# Author: Stephan Haloftis
# Student ID: 010727171

from PackageMap import *
from Fleet import *
from Utils import *
from Coords import coordinates
from Truck import Truck

import csv
import datetime
import tkinter as tk
from tkinter import ttk

# Creating a PackageMap object and loading the package list
map = PackageMap()
list = map.packagelist()
map.add(list)
packages = map.packages

# Setting time to 8:00 AM
time = datetime.datetime(2020, 1, 1, 8, 0, 0)  # 8:00 AM

# GUI Settings
WINDOW_TITLE = "Package Delivery System"
MAP_IMAGE_PATH = "map.png"
MENU_ORIGIN = [672, 756]

root = tk.Tk()
root.title(WINDOW_TITLE)
root.resizable(False, False)
root.configure(background="white")

# Load the map image
pmap = tk.PhotoImage(file=MAP_IMAGE_PATH)
w = pmap.width()
h = pmap.height()

# Create a canvas that can fit the above image
canvas = tk.Canvas(root, width=w, height=h, bg="grey")
canvas.pack(expand=tk.YES, fill=tk.BOTH)
canvas.create_image(0, 0, image=pmap, anchor=tk.NW)


# generatePath function which takes currentcoordinates, nearestcoordinates, and color as parameters
# and draws a line between the two coordinates for the GUI
def generatePath(currentcoordinates, nearestcoordinates, color):
    canvas.create_line(currentcoordinates[0], currentcoordinates[1], nearestcoordinates[0], nearestcoordinates[1], fill=color, width=3, smooth=True, arrow=tk.LAST)


# Function which populates a HashTable with data from the Package File.
# An improvement to the code would be to have to buildTable function inside the HashMap class
# But the constraints of building the HashMap class per the PA state not to use any libraries or packages
def sortload(truck):
    # Remove packages from exceptions (map.priority, map.exclusive, etc) and add to load []
    # Don't remove packages from map.packages
    try:
        # Determine if this is the last load by comparing the number of packages left in the map to the truck capacity
        lastload = False
        if len(map.packages) <= truck.capacity:
            lastload = True

        # Sort exceptions and create a list of sorted packages
        map.sortexceptions()
        sorted = []
        # sort load while len(sorted) < truck.capacity or on lastload
        while len(sorted) < truck.capacity or lastload:

            # Delayed packages
            for package in map.packages:
                # Only sort through undelivered packages
                # Use timedelta to create delay time for delayed packages
                if package.delayed:
                    minutesdelayed = package.delay
                    timedelta = datetime.timedelta(minutes=minutesdelayed)
                    delaytime = time + timedelta
                    print(f"Package {package.id} is delayed until {delaytime.time()}")

                if len(sorted) == truck.capacity:
                    return sorted

            # Grouped
            for package in map.packages:
                if package.delayed:
                    minutesdelayed = package.delay
                    timedelta = datetime.timedelta(minutes=minutesdelayed)
                    delaytime = time + timedelta
                # Add group packages to load first
                if package.group:
                    # Add to load
                    sorted.append(package)
                    map.grouped.remove(package)
                    print(f"Package {package.id} is a group package. It has been loaded.")

                if len(sorted) == truck.capacity:
                    return sorted

            # Exclusive/Priority
            for package in map.packages:
                # Remove exclusive packages from priority list
                if package.exclusive and package.priority:
                    if "Truck 2" not in truck.name:
                        map.priority.remove(package)
                        print(f"Package {package.id} is an exclusive package, but not for {truck.name}")
                    elif "Truck 2" in truck.name:
                        sorted.append(package)
                        map.priority.remove(package)
                        map.exclusive.remove(package)
                        print(f"Package {package.id} is an exclusive package. It has been loaded.")

                    if len(sorted) == truck.capacity:
                        return sorted

            # Mislabeled
            for package in map.packages:
                # Handle mislabeled package
                if package.mislabel and package.priority:
                    if time < delaytime:
                        map.priority.remove(package)
                        map.delayed.append(package)
                        print(f"Package {package.id} is mislabeled. It has been removed from priority list.")
                    else:
                        # Correct address for package 9
                        # Note: "No match found for address" error when parsing distance table till after time
                        package.address = "410 S State St"
                        package.city = "Salt Lake City"
                        package.state = "UT"
                        package.zipcode = "84111"

                        sorted.append(package)
                        map.mislabel.remove(package)
                        print(f"Package {package.id} label has been corrected. It has been loaded.")

                    if len(sorted) == truck.capacity:
                        return sorted

            # Priority
            for package in map.packages:
                # Add priority packages to load
                if package.priority:
                    sorted.append(package)
                    map.priority.remove(package)
                    print(f"Package {package.id} is a priority package")

                # # If there isn't a full load of packages left
                # elif len(sorted) < 16 and len(map.packages) == 0:
                #     return sorted
                # if not package.exception:
                #     # Add non-exception packages to load
                #     sorted.append(package)
                # # print(f"Package {package.id} is a non-exception package")

                if len(sorted) == truck.capacity:
                    return sorted

    except csv.Error as e:  # Catch any csv errors
        # Print an error message if there's a problem with the csv data
        print("Error building table")


truck1 = Truck()
truck1.name = "Truck 1"
load1 = sortload(truck1)
truck1.cargo.append(load1)

for packages in truck1.cargo:
    for package in packages:
        package.status = package.Status.OUT.value
        print(f"Package {package.id} is {package.status} on {truck1.name}.")


def deliver(truck):
    distances = []
    # While the truck has packages
    while len(truck.cargo) > 0:

        # Find the nearest neighbor
        for packages in truck.cargo:
            for package in packages:
                # print("Truck address: ", truck.address)
                # print("Package address: ", package.address)
                distance = map.calculatedistance(truck.address, package.address)
                distances.append((package, distance))

        # Filter out the None values
        # distances = list(filter(lambda x: x[1] is not None, distances))
        distance = [d for d in distances if d[1] is not None]
        if distances:
            # Find the package with the smallest distance
            nearest = min(distances, key=lambda x: x[1])

        # Change truck address to the nearest package's address
        truck.address = nearest[0].address

        # Increment the truck's mileage by the distance to the nearest package
        truck.mileage += float(nearest[1])

        # Update package status to delivered
        nearest[0].status = nearest[0].Status.DEL.value
        for packages in truck.cargo:
            for package in packages:
                if package.status == package.Status.DEL.value:
                    print(f"Package {package.id} is {package.status} on {truck.name}.")

        # Remove nearest from distances
        distances.remove(nearest)

        # Remove nearest from truck.cargo
        for packages in truck.cargo:
            for package in packages:
                if package == nearest[0]:
                    packages.remove(package)
                    print(f"Package {package.id} has been removed from {truck.name}.")


deliver(truck1)


def deliverpackages(truck, load, time):
    while len(truck.cargo) > 0:
        # Create packages and distances lists
        list = []  # tuple: (package, distance)

        # Find the distance between the truck and each package
        for load in truck.cargo:
            for package in load:
                distance = Utils.findDistance(truck.address, package.address)
                if distance is not None:
                    list.append((package, distance))

        # Find the package with the smallest distance
        nearest = min(list, key=lambda x: x[1])
        # Change truck address to the nearest package's address
        truck.address = nearest[0].address

        # Increment the truck's mileage by the distance to the nearest package
        truck.mileage += nearest[1]

        # Update the trucks coordinates
        truck.coordinates = Utils.findCoordinates(truck.address)

        # Update times
        # Calculate the duration of the trip, in hours
        duration = Utils.calculateduration(nearest[1])
        # Convert the duration to minutes
        inminutes = 60 * duration
        # Convert the minutes to a timedelta object
        duration = datetime.timedelta(minutes=inminutes)
        # Add the duration to the time
        time = time + duration

        # Update the truck's time
        truck.time += duration

        # Deliver the package NEEDS WORK HERE !!!!!!!!!!!!!!!!!
        for load in truck.cargo:
            for package in load:
                if package == nearest[0]:
                    package.timedelivered = time
                    package.status = "Delivered"
                    load.remove(package)

        # Remove from map
        map.delete(nearest[0].id)

        for load in truck.cargo:
            for package in load:
                path = (truck.address, truck.time, truck.coordinates)
                package.footprint.append(path)


# Worst Case: O(n^2)
# deliverPackages function incorporates a variant of the Greedy Algorithm
# def deliverPackages(truck, color):
#     delivered = []
#     # Continues as long as there are packages left to deliver
#     while truck.packages:
#         cords = []
#         packages = []  # Stores the packages that are to be delivered
#         distances = []  # Stores the distances from the truck to the packages
#         delivered = []  # Stores the packages that have been delivered
#         path = []  # Stores the path that the truck will take
#         # Append coordinates to cords array
#         for xy in coordinates:
#             cords.append(xy)
#         # Add distances and packages to the distances and packages lists
#         for index, packageID in enumerate(truck.packages):
#             package = workload.search(packageID)  # Retrieves the package details
#             package.coordinates = cords[index]  # Sets the package's address coordinates
#             distance = Utils.findDistance(truck.address, package.address)  # Calculates the distance from the truck to the package
#             if distance is None:
#                 distance = 0.0
#             # Adds the distance and package to the distances list
#             distances.append((distance, package))
#             # Add the package to the packages list
#             packages.append(package)
#         # Finds the package with the smallest distance to the truck
#         nearestneighbor = min(distances, key=lambda x: x[0])
#         # Increment the time by the time it takes to deliver the nearest package
#         # truck.time = Utils.calculateTimeDT(time, nearestneighbor[0])
#         truck.time = passTime(nearestneighbor[0])
#         # Update package time to truck time
#         nearestneighbor[1].time = truck.time
#         # Save current truck coordinates
#         currentcoordinates = truck.coordinates
#         # Update truck coordinates to nearest package coordinates
#         if truck.address == "4001 South 700 East":  # Hub address
#             truck.updateLocation(nearestneighbor[1].address)
#             truck.updateCoordinates(nearestneighbor[1].coordinates)
#         # Add the coordinates of the nearest package to the path with respect to the indexing scheme of the addressfile
#         path.append(nearestneighbor[1].coordinates)
#         # Finds the coordinates of the nearest package
#         nearestcoordinates = Utils.findCoordinates(nearestneighbor[1].address)
#         # Draws the path from the truck to the nearest package
#         generatePath(currentcoordinates, nearestcoordinates, color)
#         # Increases the mileage of the truck by the distance to the nearest package
#         truck.mileage += nearestneighbor[0]
#         # Updates the location of the truck to the location of the package that was just delivered
#         truck.updateLocation(nearestneighbor[1].address)
#         # Updates the coordinates of the truck to the coordinates of the package that was just delivered
#         truck.updateCoordinates(nearestcoordinates)
#         # Updates the status of the package to "Delivered"
#         nearestneighbor[1].status = Package.Status.DEL.value
#         # Adds the package to the list of delivered packages
#         delivered.append((nearestneighbor[1], nearestneighbor[1].status))
#         # Removes the delivered package from the truck's packages
#         truck.packages.remove(nearestneighbor[1].id)
#     # Returns the total mileage of the truck after all packages have been delivered
#     updateTree(tree)
#     return truck.mileage, delivered, time


# Creates a tree view of the packages
def buildTree():
    # Create a tree view with the following columns
    columns = ["Package ID", "Address", "City", "State", "Zip Code", "Deadline", "Weight", "Status", "Note"]
    tree = ttk.Treeview(root, columns=columns, show="headings")
    # Set the headings and column widths
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=74, anchor="center")
    # Insert the data into the tree view
    packagedata = [
        (
            package.id,
            package.address,
            package.city,
            package.state,
            package.zipcode,
            package.deadline,
            package.weight,
            package.status,
            package.note
        )
        for i in range(1, 41)
        for package in [workload.search(i)]
    ]
    # Insert the data into the tree view
    for i in packagedata:
        if i[7] == "Docked at Hub":
            tree.insert("", "end", values=i, tags="athub")
            tree.tag_configure('athub', background='yellow')
        if i[7] == "Processing":
            tree.insert("", "end", values=i, tags="processing")
            tree.tag_configure('processing', background='blue')
        if i[7] == "Delivered":
            tree.insert("", "end", values=i, tags="delivered")
            tree.tag_configure('delivered', background='green')
        if i[7] == "Delayed":
            tree.insert("", "end", values=i, tags="delayed")
            tree.tag_configure('delayed', background='red')
    tree.place(x=10, y=10)
    tree.pack()
    return tree


def clearTree(tree):
    tree.destroy()


# Updates the tree view after a package has been delivered
def updateTree(tree):
    tree.delete(*tree.get_children())
    # Insert the data into the tree view
    packagedata = [
        (
            package.id,
            package.address,
            package.city,
            package.state,
            package.zipcode,
            package.deadline,
            package.weight,
            package.status,
            package.note
        )
        for i in range(1, 41)
        for package in [workload.search(i)]
    ]
    # Insert the data into the tree view
    for i in packagedata:
        if i[7] == "Docked at Station":
            tree.insert("", "end", values=i, tags="athub")
            tree.tag_configure('athub', background='yellow')
        if i[7] == "Processing":
            tree.insert("", "end", values=i, tags="processing")
            tree.tag_configure('processing', background='blue')
        if i[7] == "Delivered":
            tree.insert("", "end", values=i, tags="delivered")
            tree.tag_configure('delivered', background='green')
        if i[7] == "Delayed":
            tree.insert("", "end", values=i, tags="delayed")
            tree.tag_configure('delayed', background='red')


# returnTripReport function returns the total time and mileage of the trucks after all packages have been delivered
def returnTripReport():
    trucks = [truck1, truck2, truck3]
    for truck in trucks:
        if truck.time is not None:
            totaltime = truck.time
            totaltimelabel = tk.Label(root, text=f"Total Time: {totaltime}")
            totaltimelabel.pack(side="bottom", fill="x")
    if truck1.mileage and truck2.mileage and truck3.mileage is not None:
        totalmileage = round((truck1.mileage + truck2.mileage + truck3.mileage), 2)
        totalmileagelabel = tk.Label(root, text=f"Total Mileage: {totalmileage}")
        totalmileagelabel.pack(side="bottom", fill="x")
    timepassed = totaltime - datetime.timedelta(hours=8)
    timeformatted = timepassed.strftime("%H:%M")
    print("Time passed: ", timeformatted)
    print("Time: ", totaltime.time())
    print("Mileage: ", totalmileage)
    return totalmileage, timeformatted


# searchLoad() searches for a package by ID and focuses on it in the tree view
def searchLoad(packageID, tree):
    package = workload.search(packageID)
    for child in tree.get_children():
        if tree.item(child)["values"][0] == package.id:
            tree.selection_set(child)
            tree.see(child)
            tree.focus(child)
            break
    return package

# GUI

# tree = buildTree()

searchentry = tk.Entry(root)
searchentry.place(x=MENU_ORIGIN[0] + 10, y=MENU_ORIGIN[1] - 150)

searchbutton = tk.Button(root, text="Search", command=lambda: searchLoad(int(searchentry.get()), tree))
searchbutton.place(x=MENU_ORIGIN[0] + 10, y=MENU_ORIGIN[1] - 180)
searchbutton.pack(side="bottom", fill="x", expand=True, padx=5, pady=5)
searchentry.pack(side="bottom", fill="x", expand=True, padx=5, pady=5)

truck1button = tk.Button(root, text="Truck 1", command=lambda: deliverPackages(truck1, "red"))
# truck1button.place(x=MENU_ORIGIN[0] + 10, y=MENU_ORIGIN[1] - 30)
truck1button.pack(side="bottom", fill="x", expand=True, padx=5, pady=5)

truck2button = tk.Button(root, text="Truck 2", command=lambda: deliverPackages(truck2, "blue"))
# truck2button.place(x=MENU_ORIGIN[0] + 10, y=MENU_ORIGIN[1] - 60)
truck2button.pack(side="bottom", fill="x", expand=True, padx=5, pady=5)

truck3button = tk.Button(root, text="Truck 3", command=lambda: deliverPackages(truck3, "green"))
# truck3button.place(x=MENU_ORIGIN[0] + 10, y=MENU_ORIGIN[1] - 90)
truck3button.pack(side="bottom", fill="x", expand=True, padx=5, pady=5)

calculationsbutton = tk.Button(root, text="Calculate", command=returnTripReport)
# totalmileagebutton.place(x=MENU_ORIGIN[0] + 10, y=MENU_ORIGIN[1] - 150)
calculationsbutton.pack(side="bottom", fill="x", expand=True, padx=5, pady=5)

root.mainloop()
