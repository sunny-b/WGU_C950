require 'pry'

class Truck
  MAX_PACKAGES = 14
  DRIVING_SPEED_IN_MPH = 18.0
  SECONDS_PER_HOUR = 3600.0

  attr_reader :current_time, :total_distance, :id, :start_location, :packages, :max, :delete_at

  def initialize(id, start_time, start_location)
    @id = id
    @current_time = start_time
    @start_location = start_location
    @total_distance = 0
    @max = MAX_PACKAGES
    @packages = []
  end

  def add_package(package)
    if packages.length < max
      packages << package 

      package.on_truck = true
      package.left_hub_at = current_time
    end
  end

  def deliver_packages(map, return_to_hub = true)
    puts "Truck #: #{id}"
    current_location = start_location
                      
    delivered = 0

    until packages.empty? do
      closest_package = nil
      if packages.size > 1
        closest_package = packages.sort_by! { |p| map.find_distance(current_location, p.location) }.shift
      else
        closest_package = packages.shift
      end
      closest_location =  closest_package.location

      distance = map.find_distance(current_location, closest_location)
      time_to_deliver = (distance / DRIVING_SPEED_IN_MPH) * SECONDS_PER_HOUR
      delivered_at = Time.at(current_time.to_i + time_to_deliver)

      closest_package.delivered_at = delivered_at

      current_location = closest_location
      @total_distance += distance
      self.current_time = delivered_at

      delivered += 1

      puts closest_package
    end
    
    if return_to_hub
      distance = map.find_distance(current_location, start_location)
      time_to_return = (distance / DRIVING_SPEED_IN_MPH) * SECONDS_PER_HOUR

      self.current_time = Time.at(current_time.to_i + time_to_return)
      @total_distance += distance
      self.packages = []
    end
    
    puts
  end

  def full?
    packages.size == max
  end

  def wait_at_hub(timestamp)
    self.current_time = timestamp
  end

  private

  attr_writer :current_time, :start_location, :packages 
end	
