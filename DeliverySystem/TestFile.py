from PackageMap import *

map = PackageMap()

coordinates = map.coordinates
addresslist = map.addresslist


def assigncoordinates(self):
    for package in map.sorted:
        packageaddress = package[1]
        for index, address in enumerate(addresslist):
            if packageaddress in address:
                package[9] = coordinates[index]
