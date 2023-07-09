from PackageMap import *
from Truck import *
from Fleet import *
import datetime

map = PackageMap()

gtime = datetime.datetime(2020, 1, 1, 8, 0, 0)  # 8:00 AM
testtime = datetime.datetime(2020, 1, 1, 11, 5, 0)  # 10:05 AM
for package in map.sorted:
    id = package[0]
    map.updatetime(id, gtime.time())


def sortload(truck, time):
    OFD = "Out for Delivery"
    while len(truck.cargo) < truck.capacity:
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
            if testtime >= delaytime:  # THIS NEEDS TO BE CHANGED BEFORE SUBMISSION
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
            if testtime >= delaytime:  # THIS NEEDS TO BE CHANGED BEFORE SUBMISSION
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
        sortload(truck, gtime)
    return fleet


# Load trucks in fleet
fleet = trucks()

# Checking loads of each truck in the fleet
# for truck in fleet.trucks:
#     print(truck.name + " cargo:")
#     for index, package in enumerate(truck.cargo):
#         print((index + 1), package)

# Current output:
# Truck 1 cargo:
# 1 [13, '2010 W 500 S', 'Salt Lake City', 'UT', '84104', '10:30 AM', '2 Kilos', '', ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 2 [15, '4580 S 2300 E', 'Holladay', 'UT', '84117', '9:00 AM', '4 Kilos', '', ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 3 [19, '177 W Price Ave', 'Salt Lake City', 'UT', '84115', 'EOD', '37 Kilos', '', ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 4 [9, '300 State St', 'Salt Lake City', 'UT', '84103', 'EOD', '2 Kilos', "'Wrong address listed'", ('Out for Delivery', datetime.time(8, 0)), None, 140]
# 5 [6, '3060 Lester St', 'West Valley City', 'UT', '84119', '10:30 AM', '88 Kilos', "'Delayed on flight---will not arrive to depot until 9:05 am'", ('Out for Delivery', datetime.time(8, 0)), None, 65]
# 6 [28, '2835 Main St', 'Salt Lake City', 'UT', '84115', 'EOD', '7 Kilos', "'Delayed on flight---will not arrive to depot until 9:05 am'", ('Out for Delivery', datetime.time(8, 0)), None, 65]
# 7 [40, '380 W 2880 S', 'Salt Lake City', 'UT', '84115', '10:30 AM', '45 Kilos', '', ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 8 [29, '1330 2100 S', 'Salt Lake City', 'UT', '84106', '10:30 AM', '2 Kilos', '', ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 9 [31, '3365 S 900 W', 'Salt Lake City', 'UT', '84119', '10:30 AM', '1 Kilos', '', ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 10 [37, '410 S State St', 'Salt Lake City', 'UT', '84111', '10:30 AM', '2 Kilos', '', ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 11 [2, '2530 S 500 E', 'Salt Lake City', 'UT', '84106', 'EOD', '44 Kilos', '', ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 12 [5, '410 S State St', 'Salt Lake City', 'UT', '84111', 'EOD', '5 Kilos', '', ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 13 [8, '300 State St', 'Salt Lake City', 'UT', '84103', 'EOD', '9 Kilos', '', ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 14 [11, '2600 Taylorsville Blvd', 'Salt Lake City', 'UT', '84118', 'EOD', '1 Kilos', '', ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 15 [17, '3148 S 1100 W', 'Salt Lake City', 'UT', '84119', 'EOD', '2 Kilos', '', ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 16 [22, '6351 South 900 East', 'Murray', 'UT', '84121', 'EOD', '2 Kilos', '', ('Out for Delivery', datetime.time(8, 0)), None, 0]
# Truck 2 cargo:
# 1 [3, '233 Canyon Rd', 'Salt Lake City', 'UT', '84103', 'EOD', '2 Kilos', "'Can only be on truck 2'", ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 2 [36, '2300 Parkway Blvd', 'West Valley City', 'UT', '84119', 'EOD', '88 Kilos', "'Can only be on truck 2'", ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 3 [14, '4300 S 1300 E', 'Millcreek', 'UT', '84117', '10:30 AM', '88 Kilos', "'Must be delivered with 15", ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 4 [20, '3595 Main St', 'Salt Lake City', 'UT', '84115', '10:30 AM', '37 Kilos', "'Must be delivered with 13", ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 5 [25, '5383 South 900 East #104', 'Salt Lake City', 'UT', '84117', '10:30 AM', '7 Kilos', "'Delayed on flight---will not arrive to depot until 9:05 am'", ('Out for Delivery', datetime.time(8, 0)), None, 65]
# 6 [1, '195 W Oakland Ave', 'Salt Lake City', 'UT', '84115', '10:30 AM', '21 Kilos', '', ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 7 [34, '4580 S 2300 E', 'Holladay', 'UT', '84117', '10:30 AM', '2 Kilos', '', ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 8 [4, '380 W 2880 S', 'Salt Lake City', 'UT', '84115', 'EOD', '4 Kilos', '', ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 9 [10, '600 E 900 South', 'Salt Lake City', 'UT', '84105', 'EOD', '1 Kilos', '', ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 10 [21, '3595 Main St', 'Salt Lake City', 'UT', '84115', 'EOD', '3 Kilos', '', ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 11 [24, '5025 State St', 'Murray', 'UT', '84107', 'EOD', '7 Kilos', '', ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 12 [27, '1060 Dalton Ave S', 'Salt Lake City', 'UT', '84104', 'EOD', '5 Kilos', '', ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 13 [35, '1060 Dalton Ave S', 'Salt Lake City', 'UT', '84104', 'EOD', '88 Kilos', '', ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 14 [18, '1488 4800 S', 'Salt Lake City', 'UT', '84123', 'EOD', '6 Kilos', "'Can only be on truck 2'", ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 15 [16, '4580 S 2300 E', 'Holladay', 'UT', '84117', '10:30 AM', '88 Kilos', "'Must be delivered with 13", ('Out for Delivery', datetime.time(8, 0)), None, 0]
# 16 [32, '3365 S 900 W', 'Salt Lake City', 'UT', '84119', 'EOD', '1 Kilos', "'Delayed on flight---will not arrive to depot until 9:05 am'", ('Out for Delivery', datetime.time(8, 0)), None, 65]


def deliver(truck, time):
    delivered = []
    packagequeue = []
    # Mobilize all trucks in the fleet to begin delivering packages
    for package in truck.cargo:
        packageaddress = package[1]  # address of package
        distance = calculatedistance(truck.address, packageaddress)  # distance from current address to package
        packagequeue.append((package, distance))  # add package and distance to list
        # print("The distance between " + truck.address + " and " + packageaddress + " is " + str(distance) + " miles.")

    nearest = min(packagequeue, key=lambda x: x[1])  # find nearest distance in the packagequeue
    nearestpackage = nearest[0]
    nearestaddress = nearestpackage[1]
    nearestdistance = nearest[1]

    print("The nearest package is " + str(nearestpackage[0]) + " at " + nearestaddress + " which is " + str(nearestdistance) + " miles away.")

    # Send truck to nearest address
    truck.address = nearestaddress
    print("Truck " + truck.name + " is now at " + truck.address)

    # update truck mileage
    truck.mileage += nearestdistance
    print("Truck " + truck.name + " has driven " + str(truck.mileage) + " miles.")
    print("Truck mileage: " + str(truck.mileage))

    # update package status to delivered
    for package in truck.cargo:
        if package[1] == truck.address:
            package[8] = ("Delivered", time)
            delivered.append(package)
            truck.cargo.remove(package)
            print("Package " + str(package[0]) + " has been delivered.")



for truck in fleet.trucks:
    if "Truck 1" in truck.name:
        while len(truck.cargo) > 0:
            deliver(truck, gtime)
            if len(truck.cargo) == 0:
                print(truck.name + " has delivered all packages.")
                break
    # if "Truck 2" in truck.name:
    #     while len(truck.cargo) > 0:
    #         deliver(truck, gtime)
    #         if len(truck.cargo) == 0:
    #             print(truck.name + " has delivered all packages.")
    #             break

for truck in fleet.trucks:
    print(len(truck.cargo))
