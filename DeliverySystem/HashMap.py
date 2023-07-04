import csv
from enum import Enum


# HashMap class to create HashMap objects
class HashMap:
    # Package class to create Package objects
    class Package:
        # Nested class for Package Status. Improves organization and encapsulation.
        class Status(Enum):
            HUB = "Docked at Hub"
            PRO = "Processing"
            OUT = "Out for Delivery"
            DEL = "Delivered"

        # Initializes a Package object
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
            self.coordinates = None
            self.delay = None
            self.timedelivered = None

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

    # Initialize the hash map
    def __init__(self, initial_capacity=20):
        self.packages = [[] for _ in range(initial_capacity)]

    # Insert function
    def add(self, key, value):
        # Open PackageList.csv
        with open('packagelist.csv', 'r') as packagecsv:
            packagefile = csv.reader(packagecsv)
            packagefile = list(packagecsv)

        # Loop through PackageList.csv, assign values to variables accordingly
        for packagedata in packagefile:
            packageID = int(packagedata[0])
            packageAddress = packagedata[1]
            packageCity = packagedata[2]
            packageState = packagedata[3]
            packageZip = packagedata[4]
            packageDeadline = packagedata[5]
            packageWeight = packagedata[6]
            packageStatus = packagedata[7]
            packageNote = packagedata[8]

        bucket = hash(packageID) % len(self.packages)
        packages = self.packages[bucket]

        for package in packages:
            if package.id == key:
                package.value = value
                return True

        package = self.Package(packageID, packageAddress, packageCity, packageState, packageZip, packageDeadline, packageWeight, packageStatus, packageNote)
        packages.append(package)
        return True

    # Search function
    def search(self, packageID):
        bucket = hash(packageID) % len(self.packages)
        packages = self.packages[bucket]

        for package in packages:
            if package.id == packageID:
                return package.value

        return None

    # Remove function
    def remove(self, packageID):
        bucket = hash(packageID) % len(self.packages)
        packages = self.packages[bucket]

        for package in packages:
            if package.id == packageID:
                packages.remove(package)
                return True

        return False

    def __iter__(self):
        for bucket in self.packages:
            for entry in bucket:
                yield entry
