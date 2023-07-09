from Truck import *

# Fleet class for managing Trucks
# This only exists for future development
class Fleet:
    def __init__(self):
        self.trucks = []
        self.totalmileage = 0.0 # miles
        self.starttime = "8:00 AM"
        self.timeonroad = 0.0 # hours

    def __iter__(self):
        return iter(self.trucks)

    def add(self, truck):
        self.trucks.append(truck)


# Create Fleet of trucks
fleet = Fleet()
truck1 = Truck()
truck1.name = "Truck 1"
truck2 = Truck()
truck2.name = "Truck 2"
fleet.add(truck1)
fleet.add(truck2)