"""
Develop a hash table, ***without using any additional libraries or classes***, <-- (emphasis added)
that has an insertion function that takes the following components as input
and inserts the components into the hash table:

• package ID number
• delivery address
• delivery deadline
• delivery city
• delivery zip code
• package weight
• delivery status (e.g., delivered, en route)

Personal note:
I went ahead and just added everything from the CSV file to the hash table
It's surprising how almost nobody actually did this correctly (while reading through reddit, facebook groups, github, youtube, etc)
From what I've seen, almost everyone used some type of extra class or the csv library
I'm not entirely sure if this has been noticed or not???
But the directions above are very clear not to use any additional libraries or classes
You can imagine my frustration after building this entire program and then finding out that I did it wrong
"""

import csv  # not used in PackageMap, but for distance calculations below the class


class PackageMap:
    # Below are lists of the data from the task files
    # Considering it's explicitly stated not to use other libraries or classes, I'm not sure how else to do this
    # I hand-picked the coordinates for each address using Microsoft Paint so that I could have a pretty GUI
    packagelist = [
        "1,195 W Oakland Ave,Salt Lake City,UT,84115,10:30 AM,21 Kilos,,,,,,",
        "2,2530 S 500 E,Salt Lake City,UT,84106,EOD,44 Kilos,,,,,,",
        "3,233 Canyon Rd,Salt Lake City,UT,84103,EOD,2 Kilos,'Can only be on truck 2',,,,,",
        "4,380 W 2880 S,Salt Lake City,UT,84115,EOD,4 Kilos,,,,,,",
        "5,410 S State St,Salt Lake City,UT,84111,EOD,5 Kilos,,,,,,",
        "6,3060 Lester St,West Valley City,UT,84119,10:30 AM,88 Kilos,'Delayed on flight---will not arrive to depot until 9:05 am',,,,,",
        "7,1330 2100 S,Salt Lake City,UT,84106,EOD,8 Kilos,,,,,,",
        "8,300 State St,Salt Lake City,UT,84103,EOD,9 Kilos,,,,,,",
        "9,300 State St,Salt Lake City,UT,84103,EOD,2 Kilos,'Wrong address listed',,,,,",
        "10,600 E 900 South,Salt Lake City,UT,84105,EOD,1 Kilos,,,,,,",
        "11,2600 Taylorsville Blvd,Salt Lake City,UT,84118,EOD,1 Kilos,,,,,,",
        "12,3575 W Valley Central Station bus Loop,West Valley City,UT,84119,EOD,1 Kilos,,,,,,",
        "13,2010 W 500 S,Salt Lake City,UT,84104,10:30 AM,2 Kilos,,,,,,",
        "14,4300 S 1300 E,Millcreek,UT,84117,10:30 AM,88 Kilos,'Must be delivered with 15, 19',,,,,",
        "15,4580 S 2300 E,Holladay,UT,84117,9:00 AM,4 Kilos,,,,,,",
        "16,4580 S 2300 E,Holladay,UT,84117,10:30 AM,88 Kilos,'Must be delivered with 13, 19',,,,,",
        "17,3148 S 1100 W,Salt Lake City,UT,84119,EOD,2 Kilos,,,,,,",
        "18,1488 4800 S,Salt Lake City,UT,84123,EOD,6 Kilos,'Can only be on truck 2',,,,,",
        "19,177 W Price Ave,Salt Lake City,UT,84115,EOD,37 Kilos,,,,,,",
        "20,3595 Main St,Salt Lake City,UT,84115,10:30 AM,37 Kilos,'Must be delivered with 13, 15',,,,,",
        "21,3595 Main St,Salt Lake City,UT,84115,EOD,3 Kilos,,,,,,",
        "22,6351 South 900 East,Murray,UT,84121,EOD,2 Kilos,,,,,,",
        "23,5100 South 2700 West,Salt Lake City,UT,84118,EOD,5 Kilos,,,,,,",
        "24,5025 State St,Murray,UT,84107,EOD,7 Kilos,,,,,,",
        "25,5383 South 900 East #104,Salt Lake City,UT,84117,10:30 AM,7 Kilos,'Delayed on flight---will not arrive to depot until 9:05 am',,,,,",
        "26,5383 South 900 East #104,Salt Lake City,UT,84117,EOD,25 Kilos,,,,,,",
        "27,1060 Dalton Ave S,Salt Lake City,UT,84104,EOD,5 Kilos,,,,,,",
        "28,2835 Main St,Salt Lake City,UT,84115,EOD,7 Kilos,'Delayed on flight---will not arrive to depot until 9:05 am',,,,,",
        "29,1330 2100 S,Salt Lake City,UT,84106,10:30 AM,2 Kilos,,,,,,",
        "30,300 State St,Salt Lake City,UT,84103,10:30 AM,1 Kilos,,,,,,",
        "31,3365 S 900 W,Salt Lake City,UT,84119,10:30 AM,1 Kilos,,,,,,",
        "32,3365 S 900 W,Salt Lake City,UT,84119,EOD,1 Kilos,'Delayed on flight---will not arrive to depot until 9:05 am',,,,,",
        "33,2530 S 500 E,Salt Lake City,UT,84106,EOD,1 Kilos,,,,,,",
        "34,4580 S 2300 E,Holladay,UT,84117,10:30 AM,2 Kilos,,,,,,",
        "35,1060 Dalton Ave S,Salt Lake City,UT,84104,EOD,88 Kilos,,,,,,",
        "36,2300 Parkway Blvd,West Valley City,UT,84119,EOD,88 Kilos,'Can only be on truck 2',,,,,",
        "37,410 S State St,Salt Lake City,UT,84111,10:30 AM,2 Kilos,,,,,,",
        "38,410 S State St,Salt Lake City,UT,84111,EOD,9 Kilos,'Can only be on truck 2',,,,,",
        "39,2010 W 500 S,Salt Lake City,UT,84104,EOD,9 Kilos,,,,,,",
        "40,380 W 2880 S,Salt Lake City,UT,84115,10:30 AM,45 Kilos,,,,,,"
    ]

    addresslist = [
        "0,Western Governors University,4001 South 700 East",
        "1,International Peace Gardens,1060 Dalton Ave S",
        "2,Sugar House Park,1330 2100 S",
        "3,Taylorsville-Bennion Heritage City Gov Off,1488 4800 S",
        "4,Salt Lake City Division of Health Services,177 W Price Ave",
        "5,South Salt Lake Public Works,195 W Oakland Ave",
        "6,Salt Lake City Streets and Sanitation,2010 W 500 S",
        "7,Deker Lake,2300 Parkway Blvd",
        "8,Salt Lake City Ottinger Hall,233 Canyon Rd",
        "9,Columbus Library,2530 S 500 E",
        "10,Taylorsville City Hall,2600 Taylorsville Blvd",
        "11,South Salt Lake Police,2835 Main St",
        "12,Council Hall,300 State St",
        "13,Redwood Park,3060 Lester St",
        "14,Salt Lake County Mental Health,3148 S 1100 W",
        "15,Salt Lake County United Police Dept,3365 S 900 W",
        "16,West Valley Prosecutor,3575 W Valley Central Station bus Loop",
        "17,Housing Auth. of Salt Lake County,3595 Main St",
        "18,Utah DMV Administrative Office,380 W 2880 S",
        "19,Third District Juvenile Court,410 S State St",
        "20,Cottonwood Regional Softball Complex,4300 S 1300 E",
        "21,Holiday City Office,4580 S 2300 E",
        "22,Murray City Museum,5025 State St",
        "23,Valley Regional Softball Complex,5100 South 2700 West",
        "24,City Center of Rock Springs,5383 South 900 East #104",
        "25,Rice Terrace Pavilion Park,600 E 900 South",
        "26,Wheeler Historic Farm,6351 South 900 East",
    ]

    # list of all address coordinates in the same order as address file
    coordinates = [(397, 456), (212, 185),
                   (469, 287), (184, 546),
                   (309, 424), (308, 315),
                   (130, 130), (129, 326),
                   (343, 57), (372, 320),
                   (109, 593), (326, 344),
                   (335, 111), (170, 369),
                   (216, 375), (240, 398),
                   (64, 478), (329, 420),
                   (289, 351), (336, 122),
                   (447, 490), (548, 517),
                   (337, 556), (100, 572),
                   (412, 594), (412, 140),
                   (421, 677)]

    def __init__(self):
        self.unsorted = [[] for i in range(40)]  # list of all unsorted packages
        self.sorted = []  # list of all packages sorted by truck
        self.load(PackageMap.packagelist)  # add all packages to the map upon initialization
        self.grouped, self.delayed, self.mislabeled, self.exclusive, self.deadline1030, self.deadlineEOD, self.delivered = [], [], [], [], [], [], []
        self.process()  # process all packages upon initialization
        self.sorted.sort(key=lambda x: x[0])  # sort the packages by package id, for the sake of numerical sanity
        self.assigncoordinates()  # assign coordinates to all packages

    # findindex function uses linear probing to find the index of a package in the list
    @staticmethod
    def findindex(id, list):
        index = hash(id) % len(list)
        while list[index] and list[index][0] != id:
            index = (index + 1) % len(list)
        return index

    # Load function loads all unsorted packages into the map
    def load(self, list):
        # iterate through the list of packages
        for i, row in enumerate(list):
            row = row.split(',')  # split the row into a list
            packageid = int(row[0])  # convert the package id to an int
            address = row[1]
            city = row[2]
            state = row[3]
            zipcode = row[4]
            deadline = row[5]
            weight = row[6]
            notes = row[7]
            status = ('', '08:00:00')  # tuple : (status, time)
            coordinates = None  # default None
            delay = 0  # default to 0 until processing, should be int in minutes
            # index = hash(packageid) % len(self.unsorted)  # create index for data structure
            index = self.findindex(packageid, self.unsorted)
            self.unsorted[index] = ([packageid, address, city, state, zipcode, deadline, weight, notes, status, coordinates, delay])

    # Insert function inserts a package into the PackageMap
    def insert(self, id):
        # find the index of the package to be inserted
        # index = hash(id) % len(self.sorted)
        index = self.findindex(id, self.sorted)
        self.sorted.insert(index, self.sorted[id])  # insert the package into the sorted list

    # Search function returns the package object from a given id
    def search(self, id):
        # find the index of the package to be searched
        index = hash(id) % len(self.sorted) - 1
        return self.sorted[index]

    def getaddress(self, id):
        # find the index of the package to be searched
        index = hash(id) % len(self.sorted) - 1
        return self.sorted[index][1]

    def updateaddress(self, id, address, city, state, zip):
        # find the index of the package to update
        index = hash(id) % len(self.sorted) - 1
        self.sorted[index][1] = address
        self.sorted[index][2] = city
        self.sorted[index][3] = state
        self.sorted[index][4] = zip
        print('Package', id, 'address updated.')

    def updatetime(self, id, time):
        # find the index of the package to update
        index = hash(id) % len(self.sorted) - 1
        updatedtime = (self.sorted[index][8][0], time)
        self.sorted[index][8] = updatedtime

    def updatestatus(self, id, status):
        # find the index of the package to update
        index = hash(id) % len(self.sorted) - 1
        updatedstatus = (status, self.sorted[index][8][1])
        self.sorted[index][8] = updatedstatus

    # def assigncoordinates(self):
    #     # assign coordinates to all packages
    #     for index, address in enumerate(PackageMap.addresslist):  # iterate through address list
    #         if isinstance(address, str):  # if the address is a string, ridiculous right?
    #             PackageMap.addresslist[index] = address.split(',')  # split the address into a list
    #             PackageMap.addresslist[index][0] = int(PackageMap.addresslist[index][0])  # convert the package id to an int
    #             PackageMap.coordinates[index] = (
    #             int(PackageMap.coordinates[index][0]), int(PackageMap.coordinates[index][1]))
    #             PackageMap.addresslist[index].append(
    #                 PackageMap.coordinates[index])  # add the coordinates to the address list
    #             # assign coordinates to all packages
    #             for packages in self.unsorted:
    #                 if packages[1] == PackageMap.addresslist[index][2]:  # if the address matches the package address
    #                     packages[9] = PackageMap.addresslist[index][3]  # assign the coordinates to the package

    def assigncoordinates(self):
        for package in self.sorted:
            packageaddress = package[1]
            for index, address in enumerate(self.addresslist):
                if packageaddress in address:
                    package[9] = self.coordinates[index]

    def process(self):
        # Sorting packages and exceptions
        # I found the best approach was to do this iteratively, removing packages from map.packages as they are sorted
        # This is because some packages have multiple important attributes, and some exceptions are more important than others

        # Initially had the packages that were exclusively truck 2 in this array
        # but the algo was clocking in at just over 140 miles
        # I cherry-picked packages that made sense to be delivered together to hit 136 miles.
        # There are even more options for cherry-picking, but I'll stick with this for now.
        groupedids = [3, 5, 13, 14, 15, 16, 19, 20, 21, 33, 37, 39]  # package ids that must be delivered together

        # remove grouped packages from map.packages and add to grouped list
        for ids in groupedids:
            for package in self.unsorted:
                if package[0] == ids:
                    self.grouped.append(package)

        for package in self.grouped:
            # Update status to "Processed"
            package[8] = ("Processed", "8:00 AM")
            # Find the index of the package to be inserted
            # index = hash(package[0]) % len(self.unsorted)
            index = self.findindex(package[0], self.unsorted)
            self.sorted.insert(index, package)  # insert the package into the sorted list
            self.unsorted.pop(index)  # remove the package from the unsorted list

        # remove other exceptions from map.packages and add to appropriate lists
        for package in self.unsorted:
            note = package[7]
            if "Delayed on flight" in note:
                self.delayed.append(package)
                package[10] = 65  # delayed until 9:05, 65 mintues after 8:00
                package[8] = ("Delayed on flight, expected arrival is 9:05 AM", "8:00 AM")
            # Because package 26 is delayed, it only makes sense to deliver 26 with it to save mileage
            # So remove 26 from unsorted and add it to delayed
            # The deadline for 26 is EOD so this is OK
            # Other packages that can be handled like this are 31, 33
            if package[0] == 26:
                self.delayed.append(package)
                package[10] = 65
            if "Wrong address listed" in note:
                self.mislabeled.append(package)
                package[10] = 140  # delayed until 10:20, 140 minutes after 8:00
                package[8] = ("Wrong address listed, delayed until corrected.", "8:00 AM")
            # Package 37 deadline is 10:30, 5 is EOD, both can be shipped on truck 2 with 38
            if "Can only be on truck 2" in note:
                self.exclusive.append(package)
                package[8] = ("Processed at sort facility", "8:00 AM")

        for package in self.delayed:
            # Find the index of the package to be inserted
            # index = hash(package[0]) % len(self.unsorted)
            index = self.findindex(package[0], self.unsorted)
            self.sorted.insert(index, package)  # insert the package into the sorted list
            self.unsorted.pop(index)  # remove the package from the unsorted list

        for package in self.mislabeled:
            # Find the index of the package to be inserted
            # index = hash(package[0]) % len(self.unsorted)
            index = self.findindex(package[0], self.unsorted)
            self.sorted.insert(index, package)  # insert the package into the sorted list
            self.unsorted.pop(index)  # remove the package from the unsorted list

        for package in self.exclusive:
            # Find the index of the package to be inserted
            # index = hash(package[0]) % len(self.unsorted)
            index = self.findindex(package[0], self.unsorted)
            self.sorted.insert(index, package)  # insert the package into the sorted list
            self.unsorted.pop(index)  # remove the package from the unsorted list

        # There should only be 25 packages left in map.packages at this point\
        # Now seperate packages into 3 lists based on delivery time
        for package in self.unsorted:
            deadline = package[5]
            if "10:30 AM" in deadline:
                self.deadline1030.append(package)
                package[8] = ("Processed at sort facility, expected arrival before 10:30 AM", "8:00 AM")
            if "EOD" in deadline:
                self.deadlineEOD.append(package)
                package[8] = ("Processed at sort facility, expected arrival before 5:00 PM", "8:00 AM")

        for package in self.deadline1030:
            # Find the index of the package to be inserted
            # index = hash(package[0]) % len(self.unsorted)
            index = self.findindex(package[0], self.unsorted)
            self.sorted.insert(index, package)  # insert the package into the sorted list
            self.unsorted.pop(index)  # remove the package from the unsorted list

        for package in self.deadlineEOD:
            # Find the index of the package to be inserted
            # index = hash(package[0]) % len(self.unsorted)
            index = self.findindex(package[0], self.unsorted)
            self.sorted.insert(index, package)  # insert the package into the sorted list
            self.unsorted.pop(index)  # remove the package from the unsorted list

        # All packages should be sorted at this point, return them
        # return grouped, delayed, mislabeled, exclusive, deadline1030, deadlineEOD

    # End of PackageMap class


# Finds the distance between two addresses, probably terribly inefficient
def calculatedistance(currentaddress, destinationaddress):
    dt = []

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
        distancetable = list(dt)

    currentindex = None
    destinationindex = None

    # print("Current Address: ", repr(currentaddress))
    # print("Destination Address: ", repr(destinationaddress))

    for address in PackageMap.addresslist:
        splitstring = address.split(',')  # split the address
        streetaddress = splitstring[2]  # get the street address
        addressindex = splitstring[0]  # get the index of the address in the addresslist
        # streetaddress = address[2]
        # addressindex = address[0]
        if currentaddress in streetaddress:
            currentindex = int(addressindex)
        if destinationaddress in streetaddress:
            destinationindex = int(addressindex)

    if currentindex == destinationindex:  # if the addresses are the same, return 0, very important detail
        return 0
    if currentindex > destinationindex:
        distance = distancetable[currentindex][destinationindex]
        return distance
    elif currentindex < destinationindex:
        distance = distancetable[destinationindex][currentindex]
        return distance


# Test Code
map = PackageMap()

# for package in map.sorted:
#     packageindex = map.sorted.index(package)
#     print(packageindex, package)

# Testing functions
# package21 = map.search(21)
# package21index = package21[0]
# print(package21)
# print(map.getaddress(package21index))

# Testing distance function
# package1 = map.search(1)
# package1address = map.getaddress(1)
# package2 = map.search(2)
# package2address = map.getaddress(2)
# distance = calculatedistance(package1address, package2address)
# print(distance)
