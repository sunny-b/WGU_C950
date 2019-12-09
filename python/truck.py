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

    def add_package(self, package):
        if len(self.packages) < self.max:
            self.packages.append(package)
            self.locations.add(package.destination)

            package.on_truck = True
            package.left_hub_at = self.current_time

    def is_full(self):
        return len(self.packages) == self.max

    def wait_at_hub(self, timestamp):
        self.current_time = timestamp

    def deliver_packages(self, city_map, return_to_hub=True):
        current_location = self.start_location

        while self.packages:
            self.packages = sorted(self.packages, key=city_map.find_distance_from(current_location))
            closest_package = self.packages.pop(0)
            closest_location = closest_package.destination

            distance = city_map.find_distance_between(current_location, closest_location)
            time_to_deliver = self._time_to_travel(distance)
            delivered_at = self.current_time + timedelta(seconds=time_to_deliver)

            closest_package.delivered_at = delivered_at

            current_location = closest_location
            self.total_distance += distance
            self.current_time = delivered_at

        if return_to_hub:
            distance = city_map.find_distance_between(current_location, self.start_location)
            time_to_return = self._time_to_travel(distance)

            self.current_time = self.current_time + timedelta(seconds=time_to_return)
            self.total_distance += distance
            self.packages = []
    def _time_to_travel(self, distance):
        return (distance / self.DRIVING_SPEED_IN_MPH) * self.SECONDS_PER_HOUR
