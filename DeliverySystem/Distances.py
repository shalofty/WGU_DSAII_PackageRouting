import csv


# getDistanceTable returns file object of the distance table
def loadDistanceFile():
    try:
        with open('distancetable.csv', 'r') as file:
            reader = csv.reader(file)
            reader = list(reader)
            return reader
    finally:
        file.close()


# findIndex method returns the index of the currentaddress within the given file
def findIndex(file, currentaddress):
    try:
        for index, entry in enumerate(file):
            parsedAddress = entry[0].strip()
            if parsedAddress == currentaddress:
                return index
    except csv.Error as e:
        print(e)


# findDistance function uses the indices of an arbitrary locations to find the distances between them
def findDistances(currentaddress, packageaddress):
    try:
        # Call loadDistanceFile to assign variable as returned object
        # This object is a set of lists
        file = loadDistanceFile()
        # Call findIndex function on currentaddress and packageaddress
        currentAddressIndex = findIndex(file, currentaddress)
        packageAddressIndex = findIndex(file, packageaddress)

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


currentaddress = '2300 Parkway Blvd'
packageaddress = '6351 South 900 East'
print(findDistances(packageaddress, currentaddress))
