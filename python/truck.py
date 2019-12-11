from datetime import timedelta

class Truck(object):
    MAX_PACKAGES = 14
    DRIVING_SPEED_IN_MPH = 18.0
    SECONDS_PER_HOUR = 3600.0

    def __init__(self, identifier, start_time, start_location):
        self.identifier = identifier
        self.current_time = start_time
        self.start_location = start_location
        self.total_distance = 0
        self.max = self.MAX_PACKAGES
        self.packages = []
        self.locations = set()

    # adds package to package list and the package location to a locations set: O(n)
    def add_package(self, package):
        if len(self.packages) < self.max:
            self.packages.append(package)
            self.locations.add(package.destination)

            package.on_truck = True
            package.left_hub_at = self.current_time
    
    # helper method to determine if truck is full
    # through trial and error I discovered that using 14 packages per truck instead of 16 was more optimal
    def is_full(self):
        return len(self.packages) == self.max

    def wait_at_hub(self, timestamp):
        self.current_time = timestamp

    # this is a helper method to determine if a truck can deliver a package
    # checks to see if package is on another truck, if the package can be delivered by that truck number, or if the package is ready yet
    def can_deliver(self, package):
        return not package.on_truck and self.identifier in package.truck_availability and self.current_time >= package.ready_at

    # this is the greedy algorithm that sorts the truck's package list by distance to the trucks current location
    # after the truck travels to a location, it resorts the list based on the new location
    # it does this until all the packages have been delivered
    # Time complexity: O(n^2*log(n)) - 'n' being the number of packages
    def deliver_packages(self, city_map, return_to_hub=True):
        current_location = self.start_location
        locations = list(self.locations)

        while self.packages:
            # sort locations by proximity to current location and pop of off the closest location: O(n*log(n))
            # using a location set optimizes the sort algorithm
            # if there are multiple packages at one location, only need to sort once
            locations = sorted(locations, key=city_map.distance_from(current_location))
            closest_location = locations.pop(0)
            
            distance = city_map.find_distance_between(current_location, closest_location)
            time_to_deliver = self._time_to_travel(distance)
            delivered_at = self.current_time + timedelta(seconds=time_to_deliver)
    
            # find all the packages that need to be delievered to this location: O(n)
            packages_at_location = [p for p in self.packages if p.destination.identifier == closest_location.identifier]
            for package in packages_at_location:
                package.delivered_at = delivered_at
                
                # remove package from list: O(n)
                self.packages.remove(package)

            # update current location, current time, and total distance that truck has travelled
            current_location = closest_location
            self.total_distance += distance
            self.current_time = delivered_at

        # this block is executed if the truck needs to return to the hub to get more packages
        if return_to_hub:
            distance = city_map.find_distance_between(current_location, self.start_location)
            time_to_return = self._time_to_travel(distance)

            self.current_time = self.current_time + timedelta(seconds=time_to_return)
            self.total_distance += distance

            # ensure the locations list is empty before adding more packages
            self.locations = set()


    # helper method to calculate the time to travel a particular distance
    def _time_to_travel(self, distance):
        return (distance / self.DRIVING_SPEED_IN_MPH) * self.SECONDS_PER_HOUR
