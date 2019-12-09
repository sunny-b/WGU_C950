require 'pry'
class Edge
  attr_reader :weight

  def initialize(destination, weight = 0.0)
    @destination = destination
    @weight = weight
  end

  def id
    destination.id
  end

  def name
    destination.name
  end

  def address
    destination.address
  end
  
  def packages
    destination.packages
  end

  def location
    destination
  end

  # def available_packages?(truck)
  #   packages.any? { |p| p.can_be_delivered_by?(truck) } 
  # end

  private

  attr_reader :destination
end
