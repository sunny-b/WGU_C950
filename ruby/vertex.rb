require_relative 'hash_table'

class Vertex
  attr_reader :value, :edges
  
  def initialize(location)
    @edges = HashTable.new
    @value = location
  end

  def add_edge(edge)
    edges.insert(edge.id, edge)
  end

  def find_edge(edge_id)
    edges.find(edge_id)
  end

  # def find_closest_neighbor_with_available_packages(truck)
  #   edges.find { |e| e.available_packages?(truck) }
  # end

  # def closest_neighbor
  #   edges.first
  # end
end
