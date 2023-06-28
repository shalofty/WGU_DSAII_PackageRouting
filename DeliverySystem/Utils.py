import csv
import sys
import datetime

from Coords import coordinates


# Utils file for whatever arbitrary utilities are necessary
# Helps keep codebase clean and tidy

class Utils:
    # Method getDistanceTable returns file object of the distance table
    # Replaces all empty values with 'inf', which is key during algorithm usage
    @staticmethod
    def loadDistances():
        distancetable = []
        try:
            with open('distancetable.csv', 'r') as file:
                reader = csv.reader(file, delimiter=',')
                for row in reader:
                    rowvals = []
                    for cell in row:
                        if cell:
                            rowvals.append(cell)
                        else:
                            rowvals.append(float('inf'))
                    distancetable.append(rowvals)
                reader = list(reader)
                distancetable = list(distancetable)
                return distancetable
        finally:
            file.close()

    # Method which returns a packagefile list
    @staticmethod
    def loadPackages():
        try:
            with open('packagelist.csv', 'r') as packagecsv:
                packagefile = csv.reader(packagecsv)
                packagefile = list(packagecsv)
            return packagefile
        except csv.Error as e:
            sys.exit("Error loading packages")

    # Method which returns an addressfile list
    @staticmethod
    def loadAddresses():
        try:
            with open('addressfile.csv', 'r') as addresscsv:
                addressfile = csv.reader(addresscsv)
                addressfile = list(addresscsv)
            return addressfile
        except csv.Error as e:
            sys.exit("Error loading addresses")

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

    # Method which returns distance between two locations x and y
    # findDistance function uses the indices of an arbitrary locations to find the distances between them
    @staticmethod
    def findDistance(currentaddress, packageaddress):
        try:
            # Call loadDistanceFile to assign variable as returned object
            # This object is a set of lists
            file = Utils.loadDistances()
            # Call findIndex function on currentaddress and packageaddress
            currentAddressIndex = Utils.findIndex(file, currentaddress)
            packageAddressIndex = Utils.findIndex(file, packageaddress)

            # For-loop through file, each iteration has access to an individual list
            # Use conditional logic to assign lists accordingly
            for addresslist in file:
                addressCSV = addresslist[0]
                addressCSV = addressCSV.strip()

                if addressCSV == packageaddress:
                    listPA = addresslist

                if addressCSV == currentaddress:
                    listCA = addresslist

            # Compare indices to use correct list for finding distance
            if currentAddressIndex > packageAddressIndex:
                distance = listCA[packageAddressIndex + 1]
                return float(distance)

            if packageAddressIndex > currentAddressIndex:
                distance = listPA[currentAddressIndex + 1]
                return float(distance)
        except csv.Error as e:
            print(e)

    @staticmethod
    # Method which returns the street number of an address from the addresscsv file
    def getAddress(address):
        try:
            addresscsv = Utils.loadAddresses()
            addresscsv = csv.reader(addresscsv)
            addresscsv = list(addresscsv)
            for row in addresscsv:
                # formatted = row.split(",", 3)
                if address in row[2]:
                    return row[2].strip()
            return None
        except csv.Error as e:
            sys.exit("Error getting address.")

    # Method which returns the time travelled to deliver package
    @staticmethod
    def calculateTime(distance):
        speed = 18
        time = distance / speed
        return time

    # Find coordinates of address using addressfile and Coords
    @staticmethod
    def findCoordinates(address):
        try:
            addressfile = Utils.loadAddresses()
            addressfile = csv.reader(addressfile)
            addressfile = list(addressfile)
            for index, row in enumerate(addressfile):
                if address == row[2]:
                    coords = coordinates[index]
                    return coords
            return None
        except csv.Error as e:
            sys.exit("Error getting coordinates.")


# Access utilities for distances, packages, and addresses
distancetable = Utils.loadDistances()
packagefile = Utils.loadPackages()
addressfile = Utils.loadAddresses()

# Utils.findCoordinates("410 S State St")
