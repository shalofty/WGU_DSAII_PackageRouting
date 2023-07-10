# Author: Stephan Haloftis
# Student ID: 010727171

from PackageMap import *
from Fleet import *

import datetime
import threading
import queue
import tkinter as tk
from tkinter import ttk

# Creating a PackageMap object named map
map = PackageMap()

# Create a threading lock
lock = threading.Lock()
updateq = queue.Queue()  # queue for updating the GUI

# Setting global time to 8:00 AM, time won't increment until packages start being delivered
# Also updated the times to datetime types to enable incrementing, because the task guidelines
# explicitly state not to use any additional libraries in the PackageMap class. Why?
# So they can see how creative we can be, right? Right..
gtime = datetime.datetime(2020, 1, 1, 8, 0, 0)  # 8:00 AM  # global time
testtime = datetime.datetime(2020, 1, 1, 8, 0, 0)  # 8:00 AM
for package in map.sorted:
    id = package[0]
    map.updatetime(id, gtime.time())


# generatePath function which takes currentcoordinates, nearestcoordinates, and color as parameters
# and draws a line between the two coordinates for the GUI
def generatepath(currentcoordinates, nearestcoordinates, color):
    canvas.create_line(currentcoordinates[0], currentcoordinates[1], nearestcoordinates[0], nearestcoordinates[1], fill=color, width=3, smooth=True, arrow=tk.LAST)


def sortload(truck):
    OFD = "Out for Delivery"
    lastload = False
    while len(truck.cargo) < truck.capacity or lastload:
        if (40 - len(map.delivered)) < truck.capacity:
            lastload = True
        # Add packages that are exclusive to truck 2
        # This will only happen after the first truck is already filled
        for package in map.exclusive:
            if len(truck.cargo) == truck.capacity or len(map.exclusive) == 0:
                if len(map.exclusive) == 0:
                    print("All exclusive packages have been loaded.")
                elif len(map.exclusive) > 0:
                    print("There are still " + str(len(map.exclusive)) + " exclusive packages left.")
                break
            if "Truck 2" in truck.name:
                # add exclusive packages to truck
                truck.addpackage(package)
                # update package status to "Out for Delivery"
                map.updatestatus(package[0], OFD)
                # remove package from exclusive list
                map.exclusive.remove(package)

        # Add grouped packages first, since package 15 has the earliest deadline
        for package in map.grouped:
            if len(truck.cargo) == truck.capacity or len(map.grouped) == 0:
                if len(map.grouped) == 0:
                    print("All grouped packages have been loaded.")
                elif len(map.grouped) > 0:
                    print("There are still " + str(len(map.grouped)) + " grouped packages left.")
                break
            # add grouped packages to truck
            truck.addpackage(package)
            # update package status to "Out for Delivery"
            map.updatestatus(package[0], OFD)
            # remove package from grouped list
            map.grouped.remove(package)

        # Next check the mislabeled package
        for package in map.mislabeled:
            if len(truck.cargo) == truck.capacity or len(map.mislabeled) == 0:
                if len(map.mislabeled) == 0:
                    print("All mislabeled packages have been loaded.")
                elif len(map.mislabeled) > 0:
                    print("There are still " + str(len(map.mislabeled)) + " mislabeled packages left.")
                break
            delay = package[10]
            timedelta = datetime.timedelta(minutes=delay)
            delaytime = gtime + timedelta
            if gtime >= delaytime:
                # Update the label if it's past 10:20 AM
                updatedaddress = "410 S State St"
                updatedcity = "Salt Lake City"
                updatedstate = "UT"
                updatedzip = "84111"
                map.updateaddress(package[0], updatedaddress, updatedcity, updatedstate, updatedzip)
                # add mislabeled package to truck
                truck.addpackage(package)
                # update package status to "Out for Delivery"
                map.updatestatus(package[0], OFD)
                # remove package from mislabeled list
                map.mislabeled.remove(package)

        # Next check delays
        for package in map.delayed:
            if len(truck.cargo) == truck.capacity or len(map.delayed) == 0:
                if len(map.delayed) == 0:
                    print("All delayed packages have been loaded.")
                elif len(map.delayed) > 0:
                    print("There are still " + str(len(map.delayed)) + " delayed packages left.")
                break
            delay = package[10]
            timedelta = datetime.timedelta(minutes=delay)
            delaytime = gtime + timedelta
            if gtime >= delaytime:
                # add delayed packages to truck
                truck.addpackage(package)
                # update package status to "Out for Delivery"
                map.updatestatus(package[0], OFD)
                # remove package from delayed list
                map.delayed.remove(package)

        # Next check packages with 10:30 deadline
        for package in map.deadline1030:
            if len(truck.cargo) == truck.capacity or len(map.deadline1030) == 0:
                if len(map.deadline1030) == 0:
                    print("All 10:30 packages have been loaded.")
                elif len(map.deadline1030) > 0:
                    print("There are still " + str(len(map.deadline1030)) + " 10:30 deadline packages left.")
                break
            # add packages with 10:30 deadline to truck
            truck.addpackage(package)
            # update package status to "Out for Delivery"
            map.updatestatus(package[0], OFD)
            # remove package from packages1030 list
            map.deadline1030.remove(package)

        # Next check packages with EOD deadline
        for package in map.deadlineEOD:
            if len(truck.cargo) == truck.capacity or len(map.deadlineEOD) == 0:
                if len(map.deadlineEOD) == 0:
                    print("All EOD packages have been loaded.")
                elif len(map.deadlineEOD) > 0:
                    print("There are still " + str(len(map.deadlineEOD)) + " EOD deadline packages left.")
                break
            # add packages with EOD deadline to truck
            truck.addpackage(package)
            # update package status to "Out for Delivery"
            map.updatestatus(package[0], OFD)
            # remove package from packagesEOD list
            map.deadlineEOD.remove(package)


def trucks():
    for truck in fleet.trucks:
        sortload(truck)
    return fleet


# Load trucks in fleet
fleet = trucks()


def deliver(truck, time):
    delivered = []
    urgentqueue = []
    packagequeue = []

    for package in truck.cargo:
        deadline = package[5]  # deadline of package
        if deadline == "9:00 AM" or deadline == "10:30 AM":
            urgentqueue.append(package)

    if len(urgentqueue) > 0:
        # Mobilize all trucks in the fleet to begin delivering packages
        for package in urgentqueue:
            packageaddress = package[1]  # address of package
            distance = calculatedistance(truck.address, packageaddress)  # distance from current address to package
            packagequeue.append((package, distance))  # add package and distance to list

        nearest = min(packagequeue, key=lambda x: x[1])  # find nearest distance in the packagequeue
        nearestpackage = nearest[0]  # nearest package
        nearestaddress = nearestpackage[1]  # nearest package address
        nearestcoordinates = nearestpackage[9]  # nearest package coordinates
        nearestdistance = nearest[1]  # nearest distance

        # updateq for the GUI
        updateq.put(("line", (truck.coordinates, nearestcoordinates, truck.name, truck.trip)))

        # updates truck address to the nearest package address
        truck.address = nearestaddress

        # update truck coordinates to nearest package coordinates
        truck.coordinates = nearestcoordinates

        # update truck mileage
        truck.mileage += nearestdistance

        # update time
        duration = truck.calculateduration(nearestdistance)
        timedelta = datetime.timedelta(minutes=duration)
        time += timedelta
        truck.time = time

        # update package status to delivered
        for package in urgentqueue:
            if package[1] == truck.address:
                package[8] = ("Delivered", time)  # update package status to delivered
                delivered.append(package)  # add package to delivered list
                truck.cargo.remove(package)  # remove package from truck cargo
                packagequeue.remove((package, nearestdistance))  # remove package from packagequeue
                print("Package " + str(package[0]) + " has been delivered at " + str(time.time()))
                print("The deadline was " + str(package[5]))

    if len(urgentqueue) == 0:
        # Mobilize all trucks in the fleet to begin delivering packages
        for package in truck.cargo:
            packageaddress = package[1]  # address of package
            distance = calculatedistance(truck.address, packageaddress)  # distance from current address to package
            packagequeue.append((package, distance))  # add package and distance to list

        nearest = min(packagequeue, key=lambda x: x[1])  # find nearest distance in the packagequeue
        nearestpackage = nearest[0]  # nearest package
        nearestaddress = nearestpackage[1]  # nearest package address
        nearestcoordinates = nearestpackage[9]  # nearest package coordinates
        nearestdistance = nearest[1]  # nearest distance

        # updateq for the GUI
        updateq.put(("line", (truck.coordinates, nearestcoordinates, truck.name, truck.trip)))

        # updates truck address to the nearest package address
        truck.address = nearestaddress

        # update truck coordinates to nearest package coordinates
        truck.coordinates = nearestcoordinates

        # update truck mileage
        truck.mileage += nearestdistance

        # update time
        duration = truck.calculateduration(nearestdistance)
        timedelta = datetime.timedelta(minutes=duration)
        time += timedelta
        truck.time = time

        # update package status to delivered
        for package in truck.cargo:
            if package[1] == truck.address:
                package[8] = ("Delivered", time)  # update package status to delivered
                delivered.append(package)  # add package to delivered list
                truck.cargo.remove(package)  # remove package from truck cargo
                packagequeue.remove((package, nearestdistance))  # remove package from packagequeue
                print("Package " + str(package[0]) + " has been delivered at " + str(time.time()))
                print("The deadline was " + str(package[5]))

    # End of delivery
    # add delivered packages to map.delivered
    for package in delivered:
        map.delivered.append(package)
    # when truck is empty, return to hub
    if len(truck.cargo) == 0:
        # update truck address to hub
        truck.address = "4001 South 700 East"
        # update truck coordinates to hub coordinates
        truck.coordinates = [397, 456]
        # update truck trip
        truck.trip += 1
    return time


def deliveryroutine(truck, gtime, fleet):
    while len(truck.cargo) > 0:
        with lock:
            gtime = deliver(truck, gtime)
            if len(truck.cargo) == 0:
                fleet.totalmileage += truck.mileage
                print(truck.name + " has delivered all packages.")
                print("Total mileage: " + str(fleet.totalmileage))
    return gtime


def deliverremaining(gtime):
    for package in map.delivered:
        map.sorted.remove(package)
    for truck in fleet.trucks:  # deliver the rest of the packages
        if "Truck 1" in truck.name:
            gtime = truck.time  # set time to truck 1's latest time
            for package in map.sorted:
                truck.cargo.append(package)
            while len(truck.cargo) > 0:
                gtime = deliver(truck, gtime)
                if len(truck.cargo) == 0:
                    fleet.totalmileage += truck.mileage
                    print(truck.name + " has delivered all packages.")
                    print("Total mileage: " + str(fleet.totalmileage))
                    break
    return gtime


# checkq checks the updateq for new updates to the canvas
def checkq():
    while not updateq.empty():
        command, args = updateq.get()
        if command == "line":
            truckcoordinates, nearestcoordinates, truckname, trucktrip = args
            if "Truck 1" in truckname:
                color = "red"
            elif "Truck 2" in truckname:
                color = "blue"
            if "Truck 1" in truckname and trucktrip > 0:
                color = "yellow"
            canvas.create_line(*truckcoordinates, *nearestcoordinates, fill=color, width=3, smooth=True, arrow=tk.LAST)
    root.after(100, checkq)


# In order to tackle the global time problem I decided to incorporate threading
# Truck 1 and Truck 2 run on separate threads
# Time is passed between threads, but because of how we view time in this situation it's permissible to use
# Since we're looking at the time a package was delivered
threads = []  # list of threads
for truck in fleet.trucks:  # create a thread for each truck
    thread = threading.Thread(target=deliveryroutine, args=(truck, gtime, fleet))
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

# deliver remaining packages if not all delivered
if map.delivered != 40:
    gtime = deliverremaining(gtime)

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
    package = map.search(packageID)
    for child in tree.get_children():
        if tree.item(child)["values"][0] == package.id:
            tree.selection_set(child)
            tree.see(child)
            tree.focus(child)
            break
    return package


# # GUI Settings
WINDOW_TITLE = "Package Delivery System"
MAP_IMAGE_PATH = "map.png"
MENU_ORIGIN = [672, 756]

# Create root window
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

# Start qchecker
root.after(100, checkq)

# tree = buildTree()


searchentry = tk.Entry(root)
searchentry.place(x=MENU_ORIGIN[0] + 10, y=MENU_ORIGIN[1] - 150)

searchbutton = tk.Button(root, text="Search", command=lambda: searchLoad(int(searchentry.get()), tree))
searchbutton.place(x=MENU_ORIGIN[0] + 10, y=MENU_ORIGIN[1] - 180)
searchbutton.pack(side="bottom", fill="x", expand=True, padx=5, pady=5)
searchentry.pack(side="bottom", fill="x", expand=True, padx=5, pady=5)

calculationsbutton = tk.Button(root, text="Calculate", command=returnTripReport)
calculationsbutton.pack(side="bottom", fill="x", expand=True, padx=5, pady=5)

root.mainloop()
