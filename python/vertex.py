from hash_table import HashTable

class Vertex(object):
    def __init__(self, location):
        self.edges = HashTable()
        self.value = location

    def add_edge(self, edge):
        self.edges.insert(edge.identifier, edge)

    def find_edge(self, edge_id):
        return self.edges.find(edge_id)

    def distance_to(self, location):
        return self.edges.find(location.identifier).weight
