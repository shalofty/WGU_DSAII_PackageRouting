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

def loadtruck(truck, time):
    OFD = "Out for Delivery"

    # Add packages that are exclusive to truck 2
    # This will only happen after the first truck is already filled
    for package in map.exclusive:
        if len(truck.cargo) == truck.capacity or len(map.exclusive) == 0:
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
    for package in map.packages1030:
        if len(truck.cargo) == truck.capacity or len(map.packages1030) == 0:
            break
        # add packages with 10:30 deadline to truck
        truck.addpackage(package)
        # update package status to "Out for Delivery"
        map.updatestatus(package[0], OFD)
        # remove package from packages1030 list
        map.packages1030.remove(package)

    # Next check packages with EOD deadline
    for package in map.packagesEOD:
        if len(truck.cargo) == truck.capacity or len(map.packagesEOD) == 0:
            break
        # add packages with EOD deadline to truck
        truck.addpackage(package)
        # update package status to "Out for Delivery"
        map.updatestatus(package[0], OFD)
        # remove package from packagesEOD list
        map.packagesEOD.remove(package)


def trucks():
    for truck in fleet:
        loadtruck(truck, gtime)
    return fleet

# Check to make sure packages load correctly
# for truck in fleet:
#     print(truck.name)
#     for package in truck.cargo:
#         print(package)


def deliver(time):
    gtime = time
    fleet = trucks()
    delivered = []
    distances = []
    # Mobilize all trucks in the fleet to begin delivering packages
    for truck in fleet:
        for package in truck.cargo:
            print(package)
            packageaddress = package[1]  # address of package
            distance = calculatedistance(truck.address, packageaddress)  # distance from current address to package
            distances.append((package, distance))  # add package and distance to list

        nearest = min(distances)  # find nearest package
        nearestpackage = nearest[0]
        nearestdistance = nearest[1]

        # calculate duration of trip
        duration = truck.calculateduration(nearestdistance)
        timedelta = datetime.timedelta(minutes=duration)
        deliverytime = gtime + timedelta
        gtime += timedelta  # update global time accordingly

        # update truck address to package address
        truck.address = nearestpackage[1]

        # update truck mileage
        truck.mileage += nearestdistance

        # "deliver package", remove from truck cargo
        truck.cargo.remove(nearest[0])

        # update package status to "Delivered"
        map.updatestatus(nearestpackage[0], "Delivered")

        # update the time delivered
        map.updatetime(nearestpackage[0], deliverytime.time())


for truck in fleet:
    while len(truck.cargo) > 0:
        deliver(gtime)

for truck in fleet:
    print(len(truck.cargo))
