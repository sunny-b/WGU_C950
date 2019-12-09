from hash_table import HashTable
from vertex import Vertex
from edge import Edge

class Graph(object):
    def __init__(self):
        self.vertices = HashTable(20)

    def add_vertex(self, location):
        self.vertices.insert(location.identifier, Vertex(location))

    def add_weighted_edge(self, origin, destination, weight):
        self.vertices.find(origin.identifier).add_edge(Edge(destination, weight))
        self.vertices.find(destination.identifier).add_edge(Edge(origin, weight))

    def find_vertex(self, location):
        return self.vertices.find(location.identifier)

    def find_distance_between(self, origin, target):
        return self.vertices.find(origin.identifier).distance_to(target)

    def distance_to_deliver(self, location):
        def distance_to(package):
            return self.vertices.find(location.identifier).distance_to(package.destination)

        return distance_to

    def distance_from(self, origin):
        def distance_to(destination):
            return self.vertices.find(origin.identifier).distance_to(destination)

        return distance_to
