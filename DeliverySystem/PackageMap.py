import csv
import Utils
import datetime
from datetime import datetime
from enum import Enum
from Coords import coordinates


# The PackageMap class is a HashMap that stores Package objects
# Create a PackageMap object and add/remove packages, search for packages, etc.
class PackageMap:
    # Nest the Package class inside the PackageMap class
    class Package:
        # Nested class for Package Status. Improves organization and encapsulation.
        # This idea can be expanded by have more detailed status options related to the sorting/mailing processes involved
        class Status(Enum):
            HUB = "Docked at Hub"
            OUT = "In Transit"
            DEL = "Delivered"

        # Initializes a Package object with necessary attributes
        def __init__(self, id, address, city, state, zipcode, deadline, weight, status, note):
            self.id = id
            self.address = address
            self.city = city
            self.state = state
            self.zipcode = zipcode
            self.deadline = deadline
            self.weight = weight
            self.status = self.Status.HUB.value  # everything starts at the Hub
            self.note = note
            self.coordinates = [397, 456]  # WGU coordinates
            self.exception = None  # boolean value
            self.delayed = None  # boolean value
            self.delay = None  # minutes delayed after 8:00 AM
            self.mislabel = None  # boolean value
            self.priority = None  # boolean value
            self.exclusive = None  # boolean value
            self.group = None  # boolean value
            self.timedelivered = None
            self.foreignkey = self.generatekey()  # foreign key : distance table index
            self.footprint = []  # This list will store tuples (location, time, coordinates)

        # Returns a string of the Package object
        # Without this, it will only show location in memory
        def __str__(self):
            return "%s, %s, %s, %s, %s, %s, %s, %s" % (self.id,
                                                       self.address,
                                                       self.city,
                                                       self.state,
                                                       self.zipcode,
                                                       self.deadline,
                                                       self.weight,
                                                       self.status)

        # Returns the foreign key of the Package object in relation to the distance table
        def generatekey(self):
            distancetable = PackageMap.distancetable()
            for i in range(len(distancetable)):
                if self.address == distancetable[i][0]:
                    return i

    # End of nested Package class
    # Continue with PackageMap class

    def __init__(self):
        self.packages = [[] for i in range(40)]
        self.delayed = []  # list of delayed packages
        self.mislabel = []  # list of mislabeled packages
        self.grouped = []  # list of grouped packages
        self.priority = []  # list of priority packages
        self.exclusive = []  # list of truck 2 packages
        self.distancetable = PackageMap.distancetable()
        self.addresslist = PackageMap.addresslist()
        self.packagelist = PackageMap.packagelist()

    def __iter__(self):
        return iter(self.packages)

    # add function to add a package to the PackageMap
    def add(self, list):
        for package in list:
            packageid = int(package[0])
            address = package[1]
            city = package[2]
            state = package[3]
            zipcode = package[4]
            deadline = package[5]
            weight = package[6]
            status = self.Package.Status.HUB.value
            note = package[7]
            index = hash(packageid) % len(self.packages)
            newpackage = self.Package(packageid, address, city, state, zipcode, deadline, weight, status, note)
            self.packages[index] = newpackage

    # Delete function
    def delete(self, id):
        index = hash(id) % len(self.packages)
        if self.packages[index] is not None and self.packages[index].id == id:
            self.packages[index] = None
            return True  # Package was found and deleted
        return False  # Package was not found

    # Search by package ID function returns the package object
    def searchbyid(self, id):
        index = hash(id) % len(self.packages)
        for package in self.packages:
            if package.id == id:
                return package
        return None

    # packagelist function to load the package list from CSV file
    @staticmethod
    def packagelist():
        try:
            with open('packagelist.csv', 'r') as file:
                plist = list(csv.reader(file))
            return plist
        except csv.Error as e:
            print(f"Error loading package file: {e}")

    # addresslist function to load the address list from CSV file
    @staticmethod
    def addresslist():
        try:
            with open('addressfile.csv', 'r') as file:
                alist = list(csv.reader(file))
            return alist
        except csv.Error as e:
            print(f"Error loading address list: {e}")

    # distancetable function to load the distance table from CSV file
    @staticmethod
    def distancetable():
        dt = []
        try:
            with open('distancetable.csv', 'r') as file:
                reader = csv.reader(file, delimiter=',')
                for row in reader:
                    rowvals = []
                    for cell in row[1:]:
                        if cell:
                            rowvals.append(float(cell))
                        else:
                            rowvals.append(float('inf'))
                    dt.append(rowvals)
                reader = list(reader)
                distancetable = list(dt)
                return distancetable
        except csv.Error as e:
            print(f"Error loading distance table: {e}")

    # calculatedistance function to calculate the distance between two addresses
    @staticmethod
    def calculatedistance(currentaddress, destinationaddress):
        # Load address list and distance table
        addressfile = PackageMap.addresslist()
        distancetable = PackageMap.distancetable()
        # Find the index of the current address and destination address
        cindex = PackageMap.findIndex(addresslist, currentaddress)
        dindex = PackageMap.findIndex(addresslist, destinationaddress)
        # Parse through address list. The order of the address list is the same order as the distance tables.
        for addresses in addressfile:
            parsedAddress = addresses[2].strip()
            if parsedAddress == currentaddress:
                cindex = int(addresses[0].strip())
                print("Current address index: ", cindex)
            if parsedAddress == destinationaddress:
                dindex = int(addresses[0].strip())
                print("Destination address index: ", dindex)

        # for rindex, row in enumerate(addresslist):
        #     rowparts = row.split(',')
        #     rindex = int(rowparts[0].strip())
        #     rowaddress = rowparts[2].strip()
        #     # rindex = int(row[0].strip())
        #     # rowaddress = row[2].strip()
        #     if rowaddress == currentaddress:
        #         cindex = rindex
        #     if rowaddress == destinationaddress:
        #         dindex = rindex

        # Compare indices and return their respective distance
        if cindex > dindex:
            return distancetable[cindex][dindex]
        if cindex < dindex:
            return distancetable[dindex][cindex]

    # findIndex method returns the index of the currentaddress within the given file
    @staticmethod
    def findIndex(file, currentaddress):
        try:
            for index, entry in enumerate(file):
                parsedAddress = entry[0].strip()
                if parsedAddress == currentaddress:
                    return index
        except csv.Error as e:
            print(e)

    # sortexceptions function to sort packages by exception
    # appends them to their respective lists and returns them
    # changes package booleans to True if they have an exception
    def sortexceptions(self):
        group = [13, 14, 15, 16, 19, 20]
        # Parse through all packages in data structure
        for package in self.packages:
            # Sort grouped items first
            for ids in group:
                if package.id == ids:
                    # Append to grouped list
                    self.grouped.append(package)
                    package.group = True
                    package.exception = True
            # If the package notes mention a delayed flight, update the package details
            if "Delayed on flight" in package.note:
                self.delayed.append(package)
                package.delayed = True
                package.exception = True
                package.delay = 65  # 65 minutes after 8:00 AM
            # If the package notes mention a wrong address, update the package details
            if "Wrong address listed" in package.note:
                self.mislabel.append(package)
                package.mislabel = True
                package.delayed = True
                package.exception = True
                package.delay = 140  # 140 minutes after 8:00 AM
                # There might be issues here later
            # If the package notes mention a specific truck, update the package details
            if "Can only be on truck 2" in package.note:
                self.exclusive.append(package)
                package.exclusive = True
                package.exception = True
            # If the package deadline is 10:30 AM, update the package details
            if "10:30 AM" in package.deadline:
                self.priority.append(package)
                package.priority = True
                package.exception = True
            # If the package deadline is 9:00 AM, update the package details
            if "9:00 AM" in package.deadline:
                self.priority.append(package)
                package.priority = True
                package.exception = True
            if "EOD" in package.deadline and package.note is None:
                package.exception = False

    # findcoordinates function returns the coordinates of the respective address by using the address list
    # and the coordinates list. The pixel coordinates (i.e. 436 x 236) were found by looking at the map image
    # in paint
    @staticmethod
    def findcoordinates(address):
        try:
            addressfile = PackageMap.addresslist()
            addressfile = list(addressfile)
            for index, row in enumerate(addressfile):
                if address == row[2]:
                    coords = coordinates[index]
                    return coords
            return None
        except csv.Error as e:
            print(f"Error loading address file: {e}")


distancetable = PackageMap.distancetable()
addresslist = PackageMap.addresslist()
packagelist = PackageMap.packagelist()
