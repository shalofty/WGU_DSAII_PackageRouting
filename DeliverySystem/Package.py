from PackageMap import *
from enum import Enum


# Package class to create Package objects
class Package:
    # Nested class for Package Status. Improves organization and encapsulation.
    class Status(Enum):
        HUB = "Docked at Hub"
        OUT = "Out for Delivery"
        DEL = "Delivered"

    # Initializes a Package object
    def __init__(self, id, address, city, state, zipcode, deadline, weight, status, note):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = Package.Status.HUB.value  # everything starts at the Hub ;)
        self.note = note
        self.coordinates = None
        self.delay = None
        self.timedelivered = None

    # Returns a string of the Package object
    # Without this, it will only show location in memory
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (self.id,
                                                   self.address,
                                                   self.city,
                                                   self.state,
                                                   self.zipcode,
                                                   self.deadline,
                                                   self.weight,
                                                   self.status)
