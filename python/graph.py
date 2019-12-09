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
        return self.vertices.find(origin.identifier).find_edge(target.identifier).weight

    def find_distance_from(self, location):
        def distance_to(package):
            return self.vertices.find(location.identifier).find_edge(package.destination.identifier).weight

        return distance_to
