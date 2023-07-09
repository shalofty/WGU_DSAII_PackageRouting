# Author: Stephan Haloftis
# Student ID: 010727171

from PackageMap import *
from Fleet import *

import datetime
import tkinter as tk
from tkinter import ttk

# Creating a PackageMap object
map = PackageMap()

# Setting global time to 8:00 AM, time won't increment until packages start being delivered
# Also updated the times to datetime types to enable incrementing, because the task guidelines
# explicitly state not to use any additional libraries in the PackageMap class. Why?
# So they can see how creative we can be, right? Right..
time = datetime.datetime(2020, 1, 1, 8, 0, 0)  # 8:00 AM
gtime = datetime.datetime(2020, 1, 1, 8, 0, 0)  # 8:00 AM
for package in map.sorted:
    id = package[0]
    map.updatetime(id, gtime.time())

# GUI Settings
WINDOW_TITLE = "Package Delivery System"
MAP_IMAGE_PATH = "map.png"
MENU_ORIGIN = [672, 756]

root = tk.Tk()
root.title(WINDOW_TITLE)
root.resizable(False, False)
root.configure(background="white")

# Load the map image for the GUI
pmap = tk.PhotoImage(file=MAP_IMAGE_PATH)
w = pmap.width()
h = pmap.height()

# Create a canvas that can fit the map image
canvas = tk.Canvas(root, width=w, height=h, bg="grey")
canvas.pack(expand=tk.YES, fill=tk.BOTH)
canvas.create_image(0, 0, image=pmap, anchor=tk.NW)


# generatePath function which takes currentcoordinates, nearestcoordinates, and color as parameters
# and draws a line between the two coordinates for the GUI
def generatepath(currentcoordinates, nearestcoordinates, color):
    canvas.create_line(currentcoordinates[0], currentcoordinates[1], nearestcoordinates[0], nearestcoordinates[1], fill=color, width=3, smooth=True, arrow=tk.LAST)


def loadtruck(truck, time):
    OFD = "Out for Delivery"

    # Add packages that are exclusive to truck 2
    # This will only happen after the first truck is already filled
    for package in map.exclusive:
        if len(truck.cargo) == truck.capacity or len(map.exclusive) == 0:
            break
        if "Truck 2" in truck.name:
            # add exclusive packages to truck
            truck.addpackage(package)
            # update package status to "Out for Delivery"
            map.updatestatus(package[0], OFD)

    # Add grouped packages first, since package 15 has the earliest deadline
    for package in map.grouped:
        if len(truck.cargo) == truck.capacity or len(map.grouped) == 0:
            break
        # add grouped packages to truck
        truck.addpackage(package)
        # update package status to "Out for Delivery"
        map.updatestatus(package[0], OFD)

    # Next check the mislabeled package
    for package in map.mislabeled:
        if len(truck.cargo) == truck.capacity or len(map.mislabeled) == 0:
            break
        delay = package[10]
        timedelta = datetime.timedelta(minutes=delay)
        delaytime = gtime + timedelta
        if gtime >= delaytime:  # THIS NEEDS TO BE CHANGED BEFORE SUBMISSION
            # add mislabeled package to truck
            truck.addpackage(package)
            # update package status to "Out for Delivery"
            map.updatestatus(package[0], OFD)

    # Next check delays
    for package in map.delayed:
        if len(truck.cargo) == truck.capacity or len(map.delayed) == 0:
            break
        delay = package[10]
        timedelta = datetime.timedelta(minutes=delay)
        delaytime = gtime + timedelta
        if gtime >= delaytime:  # THIS NEEDS TO BE CHANGED BEFORE SUBMISSION
            # add delayed packages to truck
            truck.addpackage(package)
            # update package status to "Out for Delivery"
            map.updatestatus(package[0], OFD)

    # Next check packages with 10:30 deadline
    for package in map.packages1030:
        if len(truck.cargo) == truck.capacity or len(map.packages1030) == 0:
            break
        # add packages with 10:30 deadline to truck
        truck.addpackage(package)
        # update package status to "Out for Delivery"
        map.updatestatus(package[0], OFD)

    # Next check packages with EOD deadline
    for package in map.packagesEOD:
        if len(truck.cargo) == truck.capacity or len(map.packagesEOD) == 0:
            break
        # add packages with EOD deadline to truck
        truck.addpackage(package)
        # update package status to "Out for Delivery"
        map.updatestatus(package[0], OFD)


# Sort packages into truck loads, change package status to "Out for delivery"
for truck in fleet:
    loadtruck(truck, time)  # load is a list of packages


# deliver function which takes truck and time as parameters
def deliver(truck, time):
    delivered = []
    distances = []
    while len(delivered) < 16:

        # Find the nearest neighbor
        for packages in truck.cargo:
            for package in packages:
                # print("Truck address: ", truck.address)
                # print("Package address: ", package.address)
                distance = map.calculatedistance(truck.address, package.address)
                distances.append((package, distance))

        # Filter out the None values
        # distances = list(filter(lambda x: x[1] is not None, distances))
        distances = [d for d in distances if d[1] is not None]
        if distances:
            # Find the package with the smallest distance
            nearest = min(distances, key=lambda x: x[1])

        # Assign the nearest package and distance to variables for better readability
        nearestpackage = nearest[0]
        nearestmileage = nearest[1]

        # Calculate the time to deliver the package
        duration = truck.calculateduration(nearestmileage)  # duration is in minutes
        timedelta = datetime.timedelta(minutes=duration)  # timedelta is in minutes
        deliverytime = time + timedelta  # delivery time
        difference = deliverytime - time  # the difference between delivery time and global time
        package.timedelivered = deliverytime  # set the package's delivery time to the delivery time
        time += timedelta  # increment the global time by the timedelta

        # Print statements for testing
        print(f"Package {nearestpackage.id} will be delivered at {deliverytime.time()}")
        print(f"{truck.name} traveled {nearestmileage} miles to deliver {nearestpackage}, in {difference} from {truck.address} to {nearestpackage.address}")

        # Assign the nearest package's coordinates
        nearestpackage.coordinates = map.findcoordinates(nearestpackage.address)

        if truck.name == "Truck 1":
            # Create path for GUI map image
            generatepath(truck.coordinates, nearestpackage.coordinates, "red")
        if truck.name == "Truck 2":
            # Create path for GUI map image
            generatepath(truck.coordinates, nearestpackage.coordinates, "blue")

        # Update truck address to the nearest package's address
        truck.address = nearestpackage.address

        # Update the truck coordinates
        truck.coordinates = map.findcoordinates(truck.address)

        # Increment the truck's mileage by the distance to the nearest package
        truck.mileage += float(nearestmileage)

        # Add nearest to delivered
        delivered.append(nearestpackage)
        print(f"Package {nearestpackage.id} has been delivered to {nearestpackage.address} at {package.timedelivered.time()}.\n")

        # Remove nearest from cargo
        truck.removepackage(nearestpackage)

        # Update package status to delivered
        nearestpackage.status = nearestpackage.Status.DEL.value

        # Remove nearest from distances
        for entry in distances:
            if nearestpackage in entry:
                print(f"Package {nearestpackage.id} has been removed from the list of distances.")
                distances.remove(entry)

        # Remove the package from map
        map.delete(nearestpackage.id)
        print(f"Package {nearestpackage.id} has been removed from the map.\n")
    print(f"{truck.name} has delivered all packages.\n")


# Deliver packages
for truck in fleet:
    deliver(truck, time)


# def deliverpackages(truck, load, time):
#     while len(truck.cargo) > 0:
#         # Create packages and distances lists
#         list = []  # tuple: (package, distance)
#
#         # Find the distance between the truck and each package
#         for load in truck.cargo:
#             for package in load:
#                 distance = Utils.findDistance(truck.address, package.address)
#                 if distance is not None:
#                     list.append((package, distance))
#
#         # Find the package with the smallest distance
#         nearest = min(list, key=lambda x: x[1])
#         # Change truck address to the nearest package's address
#         truck.address = nearest[0].address
#
#         # Increment the truck's mileage by the distance to the nearest package
#         truck.mileage += nearest[1]
#
#         # Update the trucks coordinates
#         truck.coordinates = Utils.findCoordinates(truck.address)
#
#         # Update times
#         # Calculate the duration of the trip, in hours
#         duration = Utils.calculateduration(nearest[1])
#         # Convert the duration to minutes
#         inminutes = 60 * duration
#         # Convert the minutes to a timedelta object
#         duration = datetime.timedelta(minutes=inminutes)
#         # Add the duration to the time
#         time = time + duration
#
#         # Update the truck's time
#         truck.time += duration
#
#         # Deliver the package NEEDS WORK HERE !!!!!!!!!!!!!!!!!
#         for load in truck.cargo:
#             for package in load:
#                 if package == nearest[0]:
#                     package.timedelivered = time
#                     package.status = "Delivered"
#                     load.remove(package)
#
#         # Remove from map
#         map.delete(nearest[0].id)
#
#         for load in truck.cargo:
#             for package in load:
#                 path = (truck.address, truck.time, truck.coordinates)
#                 package.footprint.append(path)


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
truck1button.pack(side="bottom", fill="x", expand=True, padx=5, pady=5)

truck2button = tk.Button(root, text="Truck 2", command=lambda: deliverPackages(truck2, "blue"))
truck2button.pack(side="bottom", fill="x", expand=True, padx=5, pady=5)

truck3button = tk.Button(root, text="Truck 3", command=lambda: deliverPackages(truck3, "green"))
truck3button.pack(side="bottom", fill="x", expand=True, padx=5, pady=5)

calculationsbutton = tk.Button(root, text="Calculate", command=returnTripReport)
calculationsbutton.pack(side="bottom", fill="x", expand=True, padx=5, pady=5)

root.mainloop()
