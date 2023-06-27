# Truck class to create Truck objects
class Truck:
    # Initializes a Truck object
    def __init__(self, capacity, speed, load, packages, mileage, address):
        self.capacity = capacity
        self.speed = speed
        self.load = load
        self.packages = packages
        self.mileage = mileage
        self.address = address  # starting location is Hub address
        self.coordinates = [397, 456]  # WGU coordinates

    # updateLocation method which changes the Truck address to currentlocation
    def updateLocation(self, currentlocation):
        self.address = currentlocation

    def updateCoordinates(self, currentcoordinates):
        self.coordinates = currentcoordinates
