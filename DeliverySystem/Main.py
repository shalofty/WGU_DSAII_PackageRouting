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
lock = threading.Lock()  # lock for updating the GUI, each truck iterates individually one after another to give the illusion of simultaneous delivery
updateq = queue.Queue()  # queue for updating the GUI

# Setting global time to 8:00 AM, time won't increment until packages start being delivered
# Also updated the times to datetime types to enable incrementing, because the task guidelines
# explicitly state not to use any additional libraries in the PackageMap class. Why?
# So they can see how creative we can be, right? Right..
gtime = datetime.datetime(2020, 1, 1, 8, 0, 0)  # 8:00 AM  # global time
for package in map.packages:
    id = package[0]
    map.updatetime(id, gtime.time())

# Original
# def trucks():
#     for truck in fleet.trucks:
#         sortload(truck)
#     return fleet


def loadtrucks():
    for truck in fleet.trucks:
        if truck.name == "Truck 1":
            load = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]
            for id in load:
                package = map.search(id)
                # print(truck.name)
                # print("Package " + str(package[0]) + " loaded onto " + truck.name + ".")
                truck.addpackage(package)
        if truck.name == "Truck 2":
            load = [3, 6, 18, 24, 25, 26, 27, 28, 32, 35, 36, 38, 39]
            for id in load:
                package = map.search(id)
                # print(truck.name)
                # print("Package " + str(package[0]) + " loaded onto " + truck.name + ".")
                truck.addpackage(package)
        if truck.name == "Truck 1" and truck.trip > 0:
            load = [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 21, 22, 23, 33]
            for id in load:
                package = map.search(id)
                # print(truck.name)
                # print("Package " + str(package[0]) + " loaded onto " + truck.name + ".")
                truck.addpackage(package)
    return fleet


# # Load trucks in fleet
fleet = loadtrucks()


def deliver(truck, time):
    delivered = []
    nottime = []
    packagequeue = []

    # Mobilize all trucks in the fleet to begin delivering packages
    for package in truck.cargo:
        packageid = package[0]  # id of package
        packageaddress = package[1]  # address of package
        deadline = package[5]  # deadline of package
        delay = package[10]  # delay of package
        if delay > 0:
            arrivaltime = gtime + datetime.timedelta(minutes=delay)  # gtime: datetime = datetime.datetime(2020, 1, 1, 8, 0, 0)
            if time < arrivaltime:
                nottime.append(package)
                continue
        if "9:00 AM" in deadline:  # if deadline is 9:00 AM, there is only 1
            distance = calculatedistance(truck.address, packageaddress)
            packagequeue.append((package, distance))
            break
        elif "10:30 AM" in deadline:
            distance = calculatedistance(truck.address, packageaddress)
            packagequeue.append((package, distance))
        else:
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
            # packagequeue.remove((package, nearestdistance))  # remove package from packagequeue
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
        map.packages.remove(package)
    for truck in fleet.trucks:  # deliver the rest of the packages
        if "Truck 1" in truck.name:
            gtime = truck.time  # set time to truck 1's latest time
            for package in map.packages:
                truck.cargo.append(package)
            while len(truck.cargo) > 0:
                gtime = deliver(truck, gtime)
                if len(truck.cargo) == 0:
                    fleet.totalmileage += truck.mileage
                    print(truck.name + " has delivered all remaining packages.")
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
            package[0],
            package[1],
            package[2],
            package[3],
            package[4],
            package[5],
            package[6],
            package[7],
            package[8]
        )
        for i in range(1, 41)
        for package in [map.search(i)]
    ]
    # Insert the data into the tree view
    for i in packagedata:
        if i[7] == "Docked at Hub":
            tree.insert("", "end", values=i, tags="athub")
            tree.tag_configure('athub', background='yellow')
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
            package[0],
            package[1],
            package[2],
            package[3],
            package[4],
            package[5],
            package[6],
            package[7],
            package[8]
        )
        for i in range(1, 41)
        for package in [map.search(i)]
    ]
    # Insert the data into the tree view
    for i in packagedata:
        if i[7] == "Docked at Hub":
            tree.insert("", "end", values=i, tags="athub")
            tree.tag_configure('athub', background='yellow')
        if i[7] == "Delivered":
            tree.insert("", "end", values=i, tags="delivered")
            tree.tag_configure('delivered', background='green')
        if i[7] == "Delayed":
            tree.insert("", "end", values=i, tags="delayed")
            tree.tag_configure('delayed', background='red')


# searchLoad() searches for a package by ID and focuses on it in the tree view
def searchmap(packageid):
    package = map.search(packageid)
    searchresult.config(text="Result: " + str(package))


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

tree = buildTree()

# Create a canvas that can fit the map image
canvas = tk.Canvas(root, width=w, height=h, bg="grey")
canvas.pack(expand=tk.YES, fill=tk.BOTH)
canvas.create_image(0, 0, image=pmap, anchor=tk.NW)

# Start qchecker
root.after(100, checkq)

searchentry = tk.Entry(root)

searchbutton = tk.Button(root, text="Search", command=lambda: searchmap(int(searchentry.get())))
searchbutton.pack(side="bottom", fill="x", expand=True, padx=5, pady=5)
searchentry.pack(side="bottom", fill="x", expand=True, padx=5, pady=5)

searchresult = tk.Label(root, text="Search Result: ", bg="white", fg="black")
searchresult.pack(side="bottom", fill="x", expand=True, padx=5, pady=5)

root.mainloop()
