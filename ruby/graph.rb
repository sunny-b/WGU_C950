class Graph
  def initialize
    @vertices = HashTable.new(20)
    @locations_hash = HashTable.new(20)
  end

  def add_vertex(location)
    vertices.insert(location.id, Vertex.new(location))
    locations_hash.insert(location.address.hash.abs, location)
  end

  def add_weighted_edge(origin, destination, weight)
    vertices.find(origin.id).add_edge(Edge.new(destination, weight))
    vertices.find(destination.id).add_edge(Edge.new(origin, weight))

    true
  end

  def find_location(address)
    locations_hash.find(address.hash.abs)
  end

  def find_distance(from, to)
    vertices.find(from.id).find_edge(to.id).weight
  end

  # def find_closest_neighbor_with_available_packages(location, truck)
  #   start_node = vertices.find(location.id)
  #   nodes_to_visit = start_node.edges.clone
  #   visited = HashTable.new(40)
  #   packages = []

  #   until nodes_to_visit.empty? || truck.full?  do
  #     node = nodes_to_visit.unshift
  #     
  #     
  #     closest = start_node.find_closest_neighbor_with_available_packages(truck)

  #   closest.nil? ? find_closest_neighbor_with_available_packages(start_node.closest_neighbor, truck) : closest.location
  # end

  private

  attr_accessor :vertices, :locations_hash
end
