from hash_table import HashTable
from vertex import Vertex
from edge import Edge

class Graph(object):
    def __init__(self):
        self.vertices = HashTable(20)

    # creates a vertex from a location and adds to vertex hash table: O(n)
    def add_vertex(self, location):
        self.vertices.insert(location.identifier, Vertex(location))

    # creates a bi-directional weighted edge between two vertexes in the graph: O(n)
    def add_weighted_edge(self, origin, destination, weight):
        self.vertices.find(origin.identifier).add_edge(Edge(destination, weight))
        self.vertices.find(destination.identifier).add_edge(Edge(origin, weight))

    # finds the vertex matching the location: O(n)
    def find_vertex(self, location):
        return self.vertices.find(location.identifier)

    # finds the distance between two vertexes: O(n)
    def find_distance_between(self, origin, target):
        return self.vertices.find(origin.identifier).distance_to(target)

    # finds the distance between a location and where the package needs to be delivered
    # similar to the method above but it used to sort the priority lists
    def distance_to_deliver(self, location):
        def distance_to(package):
            return self.vertices.find(location.identifier).distance_to(package.destination)

        return distance_to

    # creates a closure/lambda that is used to find the distances between locations
    # this is used when finding the next closest location the truck should drive to
    def distance_from(self, origin):
        def distance_to(destination):
            return self.vertices.find(origin.identifier).distance_to(destination)

        return distance_to
