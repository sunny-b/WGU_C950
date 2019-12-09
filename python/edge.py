class Edge(object):
    def __init__(self, location, weight=0.0):
        self.location = location
        self.identifier = location.identifier
        self.weight = weight

    def name(self):
        return self.location.name

    def address(self):
        return self.location.address
