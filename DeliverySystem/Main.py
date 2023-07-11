# Author: Stephan Haloftis
# Student ID: 010727171

from PackageMap import *
from Fleet import *

import datetime
import tkinter as tk
from tkinter import ttk

# Creating a PackageMap object named map
map = PackageMap()

# # GUI Settings
WINDOW_TITLE = "Package Delivery System"
MAP_IMAGE_PATH = "map.png"
MENU_ORIGIN = [672, 756]

# Create the root window
root = tk.Tk()
root.title(WINDOW_TITLE)
root.resizable(True, True)
root.configure(background="white")
root.grid_rowconfigure(0, weight=1)  # This makes the top area expandable
root.grid_columnconfigure(0, weight=1)  # This makes the whole window expandable

# Load the map image for the GUI
pmap = tk.PhotoImage(file=MAP_IMAGE_PATH)
w = pmap.width()
h = pmap.height()

# Create a canvas that can fit the map image
canvas = tk.Canvas(root, width=w, height=h, bg="grey")
# canvas.pack(expand=tk.YES, fill=tk.BOTH)
canvas.grid(row=0, column=0)
canvas.create_image(0, 0, image=pmap, anchor=tk.NW)

gtime = datetime.datetime(2020, 1, 1, 8, 0, 0)  # 8:00 AM  # global time


# drawline function I use to draw lines on the map
def drawline(currentcoordinates, destinationcoordinates, color):
    canvas.create_line(currentcoordinates[0], currentcoordinates[1], destinationcoordinates[0],
                       destinationcoordinates[1], fill=color, width=3, smooth=True, arrow=tk.LAST, dash=(1, 1))


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
            delayedtime = starttime + datetime.timedelta(
                minutes=delay)  # gtime: datetime = datetime.datetime(2020, 1, 1, 8, 0, 0)
            if time < delayedtime:
                package[12] = truck.time  # update time which package left the hub
                nottime.append(package)
                # print("Cannot deliver package " + str(packageid) + " at this time.")
                continue
        if "9:00 AM" in deadline:  # if deadline is 9:00 AM, there is only 1
            package[12] = truck.time  # update time which package left the hub
            distance = calculatedistance(truck.address, packageaddress)
            packagequeue.append((package, distance))
            break
        elif "10:30 AM" in deadline:
            package[12] = truck.time  # update time which package left the hub
            distance = calculatedistance(truck.address, packageaddress)
            packagequeue.append((package, distance))
        else:
            package[12] = truck.time  # update time which package left the hub
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
            package[8] = ("Delivered", truck.time)  # update package status to delivered
            package[11] = truck.time  # update time to package delivery time
            justdelivered.append(package)  # add package to delivered list
            truck.cargo.remove(package)  # remove package from truck cargo
            # print("Package " + str(package[0]) + " has been delivered at " + str(truck.time.time()))
            # print("The deadline was " + str(package[5]))

    # End of delivery
    # add delivered packages to map.delivered
    for package in justdelivered:
        if nearestid == package[0]:
            package[11] = truck.time  # update time to package delivery time
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
    return truck.time


# # Load trucks in fleet
fleet = loadtrucks()


# engagefleet function is used to initiate the delivery process
def engagefleet(truck, gtime, fleet):
    while len(truck.cargo) > 0:
        deliver(truck, truck.time)
        if len(truck.cargo) == 0:
            fleet.totalmileage += truck.mileage
            # print(truck.name + " has delivered all packages.\n")
            # print("Total mileage: " + str(fleet.totalmileage))


# deliverremaining function is used to deliver the remaining packages
# I could have bundled these two into one function, but this works fine and at some point
# You have to decide where to spend your time
def deliverremaining(time):
    # remove delivered packages from map.packages
    # for package in map.delivered:
    #     map.packages.remove(package)
    for truck in fleet.trucks:  # deliver the rest of the packages
        if "Truck 1" in truck.name:
            for package in map.packages:
                status = package[8][0]
                if "At hub" in status:
                    truck.cargo.append(package)
                # truck.cargo.append(package)  # add remaining packages to truck cargo
            while len(truck.cargo) > 0:
                deliver(truck, time)
                if len(truck.cargo) == 0:
                    fleet.totalmileage += truck.mileage
                    # print(truck.name + " has delivered all remaining packages.")
                    # print("Total mileage: " + str(fleet.totalmileage))
                    break


# call engagefleet on each truck in fleet
for truck in fleet.trucks:
    engagefleet(truck, gtime, fleet)

# deliver remaining packages if not all delivered
if len(map.delivered) != 40:
    time = datetime.datetime(2020, 1, 1, 10, 20, 0)
    deliverremaining(time)

# all packages are delivered, sort map.delivered by id
map.packages.sort(key=lambda x: x[0])

# Beginning of GUI functionality ----->
# Tree view of all packages, should include a scrollbar to view all packages based on time

tree = ttk.Treeview(root)  # create treeview widget

# define columns
tree["columns"] = ("ID", "Address", "Deadline", "City", "Zip", "Weight", "Status")
tree.column("#0", width=0, stretch=False)
tree.column("ID", width=40)
tree.column("Address", width=200)
tree.column("Deadline", width=100)
tree.column("City", width=100)
tree.column("Zip", width=50)
tree.column("Weight", width=50)
tree.column("Status", width=100)

# define headings
tree.heading("#0", text="")
tree.heading("ID", text="ID")
tree.heading("Address", text="Address")
tree.heading("Deadline", text="Deadline")
tree.heading("City", text="City")
tree.heading("Zip", text="Zip")
tree.heading("Weight", text="Weight")
tree.heading("Status", text="Status")

for package in map.packages:
    id = package[0]  # package id
    address = package[1]  # package address
    deadline = package[5]  # package deadline
    city = package[2]  # package city
    zipcode = package[4]  # package zipcode
    weight = package[6]  # package weight
    status = package[8][0]  # package status
    time = package[8][1]  # package delivery time
    time = time.strftime("%H:%M %p")  # format time
    tree.insert(parent="", index="end", iid=id, text="",
                values=(id, address, deadline, city, zipcode, weight, (status + " at " + time)))

# tree.pack(expand=1, side="right", fill="y")
tree.grid(row=0, column=1, rowspan=2, sticky="nsew")

# Time storing variables
slidertime = tk.StringVar()
slidertime.set("Select Time")

# Create a label to display the slider time
timelabel = tk.Label(root, textvariable=slidertime)
timelabel.grid(row=1, column=1, sticky="nsew")


# Format the slider time
def formatslidertime(minutes):
    # Convert the number of minutes into hours and minutes.
    hours = minutes // 60
    minutes %= 60
    # Use AM/PM format.
    period = 'AM' if hours < 12 else 'PM'
    hours %= 12
    if hours == 0:
        hours = 12
    return '{:02d}:{:02d} {}'.format(hours, minutes, period)


# Function to convert minutes to datetime for comparison with package delivery time
def converttotime(minutes):
    hours = minutes // 60
    minutes %= 60
    # hours %= 12
    return datetime.datetime(2020, 1, 1, hours, minutes, 0)


# This function updates the treeview based on the slider time
def updatetree(minutes):
    minutes = int(minutes)
    contime = converttotime(minutes)
    fcontime = contime.strftime("%H:%M %p")
    slidertime.set(formatslidertime(minutes))
    tree.delete(*tree.get_children())  # Remove current items in the tree
    for package in map.packages:
        id = package[0]  # package id
        address = package[1]  # package address
        deadline = package[5]  # package deadline
        city = package[2]  # package city
        zipcode = package[4]  # package zipcode
        weight = package[6]  # package weight
        lefthub = package[12]  # package left hub time
        deliverytime = package[11]
        if id == 9 and contime >= datetime.datetime(2020, 1, 1, 10, 20, 0):
            address = "410 S State St"
            city = "Salt Lake City"
            zipcode = "84111"
        if deliverytime is not None:
            fdeliverytime = deliverytime.strftime("%H:%M %p")
        status = package[8][0]  # Get package status
        if minutes < 480:
            status = "At hub"
            tree.insert(parent="", index="end", iid=id, text="",
                        values=(id, address, deadline, city, zipcode, weight, (status + " at " + fcontime)))
        elif minutes >= 480 and lefthub is not None and deliverytime is not None and contime <= deliverytime:
            status = "En route"
            tree.insert(parent="", index="end", iid=id, text="",
                        values=(id, address, deadline, city, zipcode, weight, (status + " at " + fcontime)))
        elif minutes >= 480 and deliverytime is not None and contime >= deliverytime:
            status = "Delivered"
            tree.insert(parent="", index="end", iid=id, text="",
                        values=(id, address, deadline, city, zipcode, weight, (status + " at " + fdeliverytime)))
        else:
            pass
            # print(f"Package {id} has an invalid status.")
            # print(f"Package {id} has a status of {status}.")
            # print(f"Package {id} has a delivery time of {deliverytime}.")
            # print(f"Package {id} has a left hub time of {lefthub}.")


# Create a slider to select the time
hourslider = tk.Scale(root, from_=0, to=1439, orient="vertical", length=200, command=updatetree)
hourslider.grid(row=0, column=2, sticky="nsew")


# End of treeview widget ----->


# Beginning of search widget ----->
# searchmap function is used to search for a package by id
# it is tied to the searchentry and searchbutton widgets
def searchmap(packageid):
    # make sure package id is a number
    if packageid.isdigit():
        packageid = int(packageid)
    else:
        return "Please enter a package ID."
    package = map.search(packageid)  # search for package by id
    id = package[0]  # package id
    address = package[1]  # package address
    deadline = package[5]  # package deadline
    city = package[2]  # package city
    zipcode = package[4]  # package zipcode
    weight = package[6]  # package weight
    status = package[8][0]  # package status
    time = package[8][1]  # package delivery time
    time = time.strftime("%H:%M %p")  # format time

    idlabel.config(text="ID: " + str(id))
    addresslabel.config(text="Address: " + str(address))
    deadlinelabel.config(text="Deadline: " + str(deadline))
    citylabel.config(text="City: " + str(city))
    zipcodelabel.config(text="Zipcode: " + str(zipcode))
    weightlabel.config(text="Weight: " + str(weight))
    statuslabel.config(text="Status: " + str(status) + " at " + str(time))


searchframe = tk.Frame(root)
searchframe.grid(row=1, column=0, sticky="nsew")

searchentry = tk.Entry(searchframe)
searchentry.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
searchbutton = tk.Button(searchframe, text="Search", command=lambda: searchmap(searchentry.get()))
searchbutton.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

labelFrame = tk.Frame(searchframe)
labelFrame.grid(row=2, column=0, sticky="nsew")

idlabel = tk.Label(labelFrame, text="ID: ", bg="white", fg="black")
idlabel.grid(row=0, column=2, sticky="w")
addresslabel = tk.Label(labelFrame, text="Address: ", bg="white", fg="black")
addresslabel.grid(row=0, column=3, sticky="w")
deadlinelabel = tk.Label(labelFrame, text="Deadline: ", bg="white", fg="black")
deadlinelabel.grid(row=0, column=4, sticky="w")
citylabel = tk.Label(labelFrame, text="City: ", bg="white", fg="black")
citylabel.grid(row=0, column=5, sticky="w")
zipcodelabel = tk.Label(labelFrame, text="Zipcode: ", bg="white", fg="black")
zipcodelabel.grid(row=0, column=6, sticky="w")
weightlabel = tk.Label(labelFrame, text="Weight: ", bg="white", fg="black")
weightlabel.grid(row=0, column=7, sticky="w")
statuslabel = tk.Label(labelFrame, text="Status: ", bg="white", fg="black")
statuslabel.grid(row=0, column=8, sticky="w")

# End of Search Feature ----->
# Beginning of total mileage ----->

totalmileagelabel = tk.Label(labelFrame, text="Total Mileage: ", bg="white", fg="black")
totalmileagelabel.grid(row=2, column=1, sticky="w")


def gettotalmileage():
    totalmileage = fleet.totalmileage
    totalmileagelabel.config(text="Total Mileage: " + str(totalmileage) + " miles")


gettotalmileage()

root.mainloop()
