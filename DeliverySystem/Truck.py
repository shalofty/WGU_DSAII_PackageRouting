import datetime
import Utils


# Truck class to create Truck objects
class Truck:
    # Initializes a Truck object
    def __init__(self):
        self.name = None
        self.capacity = 16  # packages
        self.speed = 18  # miles per hour
        self.cargo = []  # list of Package objects
        self.loaded = None  # boolean
        self.mileage = 0.0  # miles
        self.footprint = []  # Tuple of (location, time)
        self.address = "4001 South 700 East"  # starting location is Hub address
        self.coordinates = [397, 456]  # WGU coordinates
        self.time = datetime.datetime(2020, 1, 1, 8, 0, 0)  # starting time is 8:00 AM

    # updateLocation method which changes the Truck address to currentlocation
    def updateLocation(self, currentlocation):
        self.address = currentlocation

    # updateCoordinates method which changes the Truck coordinates to currentcoordinates
    def updateCoordinates(self, currentcoordinates):
        self.coordinates = currentcoordinates

    # updateMileage method which changes the Truck mileage to currentmileage
    def updateTime(self, currenttime):
        self.time = currenttime
