# Author: Stephan Haloftis
# Student ID: 010727171

from PackageMap import *
from Fleet import *

import datetime
import tkinter as tk

# Creating a PackageMap object named map
map = PackageMap()

# # GUI Settings
WINDOW_TITLE = "Package Delivery System"
MAP_IMAGE_PATH = "map.png"
MENU_ORIGIN = [672, 756]

# Create the root window
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

gtime = datetime.datetime(2020, 1, 1, 8, 0, 0)  # 8:00 AM  # global time


# drawline function I use to draw lines on the map
def drawline(currentcoordinates, destinationcoordinates, color):
    canvas.create_line(currentcoordinates[0], currentcoordinates[1], destinationcoordinates[0], destinationcoordinates[1], fill=color, width=3, smooth=True, arrow=tk.LAST, dash=(1, 1))


# loadtrucks function manually loads packages onto trucks, and returns a fleet object
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


# The delivery function used to handle package deliveries
def deliver(truck, time):
    justdelivered = []
    nottime = []
    packagequeue = []

    # Mobilize all trucks in the fleet to begin delivering packages
    for package in truck.cargo:
        packageid = package[0]  # id of package
        packageaddress = package[1]  # address of package
        deadline = package[5]  # deadline of package
        delay = package[10]  # delay of package
        package[8] = ("En Route", truck.time)  # update package status to en route
        if delay > 0:
            starttime = datetime.datetime(2020, 1, 1, 8, 0, 0)
            delayedtime = starttime + datetime.timedelta(minutes=delay)  # gtime: datetime = datetime.datetime(2020, 1, 1, 8, 0, 0)
            if time < delayedtime:
                nottime.append(package)
                # print("Cannot deliver package " + str(packageid) + " at this time.")
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

    if len(packagequeue) > 0:
        nearest = min(packagequeue, key=lambda x: x[1])  # find nearest distance in the packagequeue
        nearestpackage = nearest[0]  # nearest package
        nearestid = nearestpackage[0]  # nearest package id
        nearestaddress = nearestpackage[1]  # nearest package address
        nearestcoordinates = nearestpackage[9]  # nearest package coordinates
        nearestdistance = nearest[1]  # nearest distance

        # draw lines according to truck
        if truck.name == "Truck 1" and truck.trip == 0:
            color = "red"
        elif truck.name == "Truck 2":
            color = "blue"
        elif truck.name == "Truck 1" and truck.trip > 0:
            color = "yellow"
        drawline(truck.coordinates, nearestcoordinates, color)

        # updates truck address to the nearest package address
        truck.address = nearestaddress
        # update truck coordinates to nearest package coordinates
        truck.coordinates = nearestcoordinates
        # update truck mileage
        truck.mileage += nearestdistance
        # update time
        duration = truck.calculateduration(nearestdistance)  # duration of trip
        timedelta = datetime.timedelta(minutes=duration)  # timedelta of trip
        truck.time += timedelta  # update truck time

    # update package status to delivered
    for package in truck.cargo:
        if package[1] == truck.address:
            package[8] = ("Delivered", time)  # update package status to delivered
            justdelivered.append(package)  # add package to delivered list
            truck.cargo.remove(package)  # remove package from truck cargo
            # packagequeue.remove((package, nearestdistance))  # remove package from packagequeue
            print("Package " + str(package[0]) + " has been delivered at " + str(truck.time.time()))
            print("The deadline was " + str(package[5]))

    # End of delivery
    # add delivered packages to map.delivered
    for package in justdelivered:
        if nearestid == package[0]:
            package[11] = time  # update time to package delivery time
        map.delivered.append(package)
    # when truck is empty, return to hub
    # the instructors in the course chatter said this wasn't necessary, but it is for the GUI
    if len(truck.cargo) == 0:
        # update truck address to hub
        truck.address = "4001 South 700 East"
        # update truck coordinates to hub coordinates
        truck.coordinates = [397, 456]
        # update truck trip
        truck.trip += 1
    return time


# # Load trucks in fleet
fleet = loadtrucks()

# engagefleet function is used to initiate the delivery process
def engagefleet(truck, gtime, fleet):
    while len(truck.cargo) > 0:
        deliver(truck, truck.time)
        if len(truck.cargo) == 0:
            fleet.totalmileage += truck.mileage
            print(truck.name + " has delivered all packages.\n")
            print("Total mileage: " + str(fleet.totalmileage))

# deliverremaining function is used to deliver the remaining packages
# I could have bundled these two into one function, but this works fine and at some point
# You have to decide where to spend your time
def deliverremaining(time):
    # remove delivered packages from map.packages
    for package in map.delivered:
        map.packages.remove(package)
    for truck in fleet.trucks:  # deliver the rest of the packages
        if "Truck 1" in truck.name:
            for package in map.packages:
                truck.cargo.append(package)  # add remaining packages to truck cargo
            while len(truck.cargo) > 0:
                deliver(truck, time)
                if len(truck.cargo) == 0:
                    fleet.totalmileage += truck.mileage
                    print(truck.name + " has delivered all remaining packages.")
                    print("Total mileage: " + str(fleet.totalmileage))
                    break


# call engagefleet on each truck in fleet
for truck in fleet.trucks:
    engagefleet(truck, gtime, fleet)

# deliver remaining packages if not all delivered
if len(map.delivered) != 40:
    time = datetime.datetime(2020, 1, 1, 10, 20, 0)
    deliverremaining(time)


root.mainloop()
