import csv
from datetime import timedelta

from package import Package
from location import Location
from hash_table import HashTable
from graph import Graph
from truck import Truck


class PackageDeliverySystem(object):
    @staticmethod

    # run is the main function that executes the entire package delivery program
    def run():
        graph = Graph()
        locations_hash = HashTable(20)
        packages_hash = HashTable(40)

        # loading all the location data from the csv file
        # populating a hash table and graph with the location data
        with open('location_data.csv') as csvfile:
            location_data = csv.reader(csvfile)

            # looping through location data: O(n)
            for data_row in location_data:
                location = Location(*data_row)

                # inserting location data into hash table: O(n)
                locations_hash.insert(location.identifier, location)
                locations_hash.insert(location.address, location)

                # creating graph vertexes from the location data: O(n)
                graph.add_vertex(location)

        all_packages = []
        high_priority = []
        low_priority = []

        # this section loops through all the package data and creates three lists: high and low priority, and a list of all packages
        with open('package_data.csv') as csvfile:
            package_data = csv.reader(csvfile)

            for data_row in package_data:
                package = Package(*(data_row+[locations_hash.find(data_row[1])]))

                all_packages.append(package)
                packages_hash.insert(package.identifier, package)

                # packages are divided into high or low priority lists depending on whether they have approaching deadlines or special instructions
                # append operations are O(1)
                if package.is_high_priority():
                    high_priority.append(package)
                else:
                    low_priority.append(package)

        # this loops through all the distance data between locations
        # This data is used to create edges between the vertexes in the graph
        with open('distance_data.csv') as csvfile:
            distance_data = csv.reader(csvfile)

            # Looping through each cell in the csv file: O(n^2)
            for i, data_row in enumerate(distance_data):
                for j, data in enumerate(data_row):
                    if data != '':

                        # adding a weighted edge to the graph: O(n) 
                        graph.add_weighted_edge(locations_hash.find(i),
                                                locations_hash.find(j),
                                                float(data))

        start_time = timedelta(hours=8)
        start_location = locations_hash.find(0)

        # only use two trucks. First truck will make two trips.
        trucks = [
            Truck(1, start_time, start_location),
            Truck(2, start_time, start_location)
        ]

        # list of times when trucks should wait to leave the station in order to optimize package distribution
        times_to_leave_hub = [
            timedelta(hours=8),
            timedelta(hours=9, minutes=5),
            timedelta(hours=10, minutes=20)
        ]

        # sort high and low priority lists based on their distance from the main hub: O(n*log(n))
        high_priority = sorted(high_priority, key=graph.distance_to_deliver(start_location))
        low_priority = sorted(low_priority, key=graph.distance_to_deliver(start_location))

        count = 0
        truck_idx = 0
        i = 0

        # continous loop until all packages have been delivered. Three loops in total
        while count < len(all_packages):
            truck = trucks[truck_idx]
            
            if i < len(times_to_leave_hub):
                leave_hub_at = times_to_leave_hub[i]
                truck.wait_at_hub(leave_hub_at)
            
            # filter priority lists based on which packages the given truck can deliver: O(n)
            filtered_high = [p for p in high_priority if truck.can_deliver(p)]

            # take as many high priorty packages as the truck can fit first
            for package in filtered_high:
                # appending a package to the truck list: O(1)
                truck.add_package(package)
                count += 1

                if truck.is_full():
                    break

            # if the truck isn't full yet, fill it up with nearby low priority packages
            if truck.is_full() is not True:
                filtered_low = [p for p in low_priority if truck.can_deliver(p)]
                for package in filtered_low: 
                    truck.add_package(package)
                    count += 1

                    if truck.is_full():
                        break

            # truck delivers packages using a greedy algorithm to find the most optimized path through the graph
            # Time complexity: O(n^2*log(n))
            truck.deliver_packages(graph, (len(all_packages) - count) > truck.max)
            i += 1
            truck_idx = i % len(trucks)

        def total_distance(truck):
            return truck.total_distance

        return [sum(map(total_distance, trucks)), packages_hash, all_packages]
