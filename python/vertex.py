from hash_table import HashTable

class Vertex(object):
    def __init__(self, location):
        self.edges = HashTable()
        self.value = location

    # add edge to hash table: O(n)
    def add_edge(self, edge):
        self.edges.insert(edge.identifier, edge)

    # find edge from id: O(n)
    def find_edge(self, edge_id):
        return self.edges.find(edge_id)

    # find distance to a neighboring vertex: O(n)
    def distance_to(self, location):
        return self.edges.find(location.identifier).weight
