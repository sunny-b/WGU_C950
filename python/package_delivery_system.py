import csv
from datetime import timedelta

from package import Package
from location import Location
from hash_table import HashTable
from graph import Graph
from truck import Truck


class PackageDeliverySystem(object):
    @staticmethod
    def run():
        graph = Graph()
        locations_hash = HashTable(20)
        packages_hash = HashTable(40)

        with open('location_data.csv') as csvfile:
            location_data = csv.reader(csvfile)

            for data_row in location_data:
                location = Location(*data_row)

                locations_hash.insert(location.identifier, location)
                locations_hash.insert(location.address, location)

                graph.add_vertex(location)

        all_packages = []
        high_priority = []
        low_priority = []

        with open('package_data.csv') as csvfile:
            package_data = csv.reader(csvfile)

            for data_row in package_data:
                package = Package(*(data_row+[locations_hash.find(data_row[1])]))

                all_packages.append(package)
                packages_hash.insert(package.identifier, package)

                if package.is_high_priority():
                    high_priority.append(package)
                else:
                    low_priority.append(package)

        with open('distance_data.csv') as csvfile:
            distance_data = csv.reader(csvfile)

            for i, data_row in enumerate(distance_data):
                for j, data in enumerate(data_row):
                    if data != '':
                        graph.add_weighted_edge(locations_hash.find(i),
                                                locations_hash.find(j),
                                                float(data))

        start_time = timedelta(hours=8)
        start_location = locations_hash.find(0)

        trucks = [
            Truck(1, start_time, start_location),
            Truck(2, start_time, start_location)
        ]

        times_to_leave_hub = [
            timedelta(hours=8),
            timedelta(hours=9, minutes=5),
            timedelta(hours=10, minutes=20)
        ]

        high_priority = sorted(high_priority, key=graph.distance_to_deliver(start_location))
        low_priority = sorted(low_priority, key=graph.distance_to_deliver(start_location))

        count = 0
        truck_idx = 0
        i = 0

        while count < len(all_packages):
            truck = trucks[truck_idx]
            
            if i < len(times_to_leave_hub):
                leave_hub_at = times_to_leave_hub[i]
                truck.wait_at_hub(leave_hub_at)
            
            filtered_high = [p for p in high_priority if truck.can_deliver(p)]
            for package in filtered_high:
                truck.add_package(package)
                count += 1

                if truck.is_full():
                    break

            if truck.is_full() is not True:
                filtered_low = [p for p in low_priority if truck.can_deliver(p)]
                for package in filtered_low: 
                    truck.add_package(package)
                    count += 1

                    if truck.is_full():
                        break

            truck.deliver_packages(graph, (len(all_packages) - count) > truck.max)
            i += 1
            truck_idx = i % len(trucks)

        def total_distance(truck):
            return truck.total_distance

        return [sum(map(total_distance, trucks)), packages_hash, all_packages]
