import datetime

# Truck class to create Truck objects
class Truck:
    # Initializes a Truck object
    def __init__(self, capacity, speed, load, packages, mileage, address):
        self.name = None
        self.capacity = capacity
        self.speed = speed
        self.load = load
        self.packages = packages
        self.mileage = mileage
        self.address = address  # starting location is Hub address
        self.coordinates = [397, 456]  # WGU coordinates
        self.time = datetime.datetime(2020, 1, 1, 8, 0, 0)  # starting time is 8:00 AM

    # updateLocation method which changes the Truck address to currentlocation
    def updateLocation(self, currentlocation):
        self.address = currentlocation

    def updateCoordinates(self, currentcoordinates):
        self.coordinates = currentcoordinates
