require 'csv'
require 'pry'
require_relative 'package'
require_relative 'location'
require_relative 'hash_table'
require_relative 'graph'
require_relative 'vertex'
require_relative 'edge'
require_relative 'truck'

class PackageDeliveryService
  def self.run
    graph = Graph.new

    location_data = CSV.read('./WGUDistanceNameData.csv', headers: false, converters: :numeric)
    locations_hash = HashTable.new

    location_data.each do |data|
      location = Location.new(*data)

      locations_hash.insert(location.id, location)
      graph.add_vertex(location)
    end

    package_data = CSV.read('./WGUInputData.csv', headers: false, converters: :numeric)
    all_packages = []
    high_priority = []
    low_priority = []

    package_data.each do |data|
      package = Package.new(*data, graph.find_location(data[1]))

      all_packages << package

      if package.high_priority?
        high_priority << package
      else
        low_priority << package
      end
    end

    distance_data = CSV.read('./WGUDistanceData.csv', headers: false, converters: :numeric)
    all_distances = []

    distance_data.each_with_index do |data, i|
     data.each_with_index do |distance, j|
       graph.add_weighted_edge(locations_hash.find(i), locations_hash.find(j), distance) unless distance.nil?
     end
    end

    trucks = [
      Truck.new(1, Time.new(2010, 10, 10, 8), locations_hash.find(0)),
      Truck.new(2, Time.new(2010, 10, 10, 9, 5), locations_hash.find(0)),
    ]

    count = 0
    truck_idx = 0
    i = 0

    times_to_leave_hub = [
      Time.new(2010, 10, 10, 8),
      Time.new(2010, 10, 10, 9, 5),
      Time.new(2010, 10, 10, 10, 20)
    ]

    high_priority.sort_by! { |p| graph.find_distance(locations_hash.find(0), p.location) }
    low_priority.sort_by! { |p| graph.find_distance(locations_hash.find(0), p.location) }

    while count < all_packages.size do
      truck = trucks[truck_idx]
      leave_hub_at = times_to_leave_hub[i]

      unless leave_hub_at.nil?
        truck.wait_at_hub(leave_hub_at)
      end

      high_priority.select { |p| p.can_be_delivered_by?(truck) }.each do |p|
        truck.add_package(p)
        count += 1

        break if truck.full?
      end

      unless truck.full?
        low_priority.select { |p| p.can_be_delivered_by?(truck) }.each do |p|
          truck.add_package(p)
          count += 1

          break if truck.full?
        end
      end

      truck.deliver_packages(graph, (all_packages.size - count) > 16)

      truck_idx = (i + 1) % trucks.size
      i += 1
    end

    trucks.sum { |t| t.total_distance }
  end
end

# def find_closest_package(packages, truck, graph)
#   packages.select { |p| p.can_be_delivered_by?(truck) }
#           .sort_by { |p| graph.find_distance(truck.start_location, graph.find_location(p.street)) }
#           .first
# end
# 
# def load_truck(truck, packages, graph)
#   current_location = truck.start_location
# 
#   until truck.full? do
#     closest_neighbor = graph.find_closest_neighbor_with_available_packages(current_location, truck)
# 
#     closest_neighbor.packages.select { |p| p.can_be_delivered_by?(truck) }.each do |package|
#       truck.add_package(package)
#       break if truck.full?
#     end
# 
#     current_location = closest_neighbor
#   end
# end

