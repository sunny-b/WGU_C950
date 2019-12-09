class Edge(object):
    def __init__(self, location, weight=0.0):
        self.location = location
        self.identifier = location.identifier
        self.weight = weight
