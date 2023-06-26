from Truck import *

# Fleet class for managing Trucks
class Fleet:
    def __init__(self):
        self.trucks = []

    def add(self, truck):
        self.trucks.append(truck)

    def remove(self, truck):
        self.trucks.remove(truck)


# Create truck objects populated with specific packages
# Each truck has specific packages to deliver
# Refer to package notes for delivery details
hub = "4001 South 700 East"
truck1 = Truck(16, 18, None, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], 0.0, hub)
truck2 = Truck(16, 18, None, [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], 0.0, hub)
truck3 = Truck(16, 18, None, [2, 4, 5, 7, 8, 9, 10, 11, 25, 28, 32, 33], 0.0, hub)

# Create fleet and add truck objects to it
fleet = Fleet()
fleet.add(truck1)
# fleet.add(truck2)
# fleet.add(truck3)
