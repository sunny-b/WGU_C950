class Package
  EOD_TIMESTAMP = Time.new(2010, 10, 10, 17)

  attr_reader :id, :street, :city, :state, :zip, :deadline, :weight_in_kilos, :delivered_at, :ready_at, :location
  attr_accessor :on_truck, :left_hub_at, :delivered_at
  
  def initialize(id, street, city, zip, deadline, weight_in_kilos, special_instructions, location)
    @id = id
    @street = street
    @city = city
    @zip = zip
    @location = location
    @deadline = convert_to_timestamp(deadline)
    @weight_in_kilos = weight_in_kilos
    @delivered_at = nil
    @ready_at = Time.new(2010, 10, 10, 8)
    @left_hub_at = nil
    @on_truck = false
    @truck_availability = [1, 2]
    @special_instructions = special_instructions
    
    modify(special_instructions)
  end

  def has_deadline?
    deadline < EOD_TIMESTAMP
  end

  def high_priority?
    has_deadline? || special_instructions != 'None' || [13, 15, 19].include?(id)
  end

  def can_be_delivered_by?(truck)
   !on_truck && truck_availability.include?(truck.id) && truck.current_time >= ready_at
  end

  def to_s
    "ID: #{id}, Location: #{street}, Deadline: #{deadline}, Ready At: #{ready_at}, Left Hub At: #{left_hub_at}, Delivered At: #{delivered_at}, Instructions: #{special_instructions}, Delivered On Time: #{delivered_at <= deadline}"
  end

  private

  attr_reader :special_instructions
  attr_writer :street, :ready_at, :zip
  attr_accessor :truck_availability

  def convert_to_timestamp(deadline)
    return Time.new(2010, 10, 10, 17) if deadline == 'EOD'

    h_m_s = deadline.split(':')
    
    hour = h_m_s[0].to_i
    min = h_m_s[1].to_i
    sec = h_m_s[2].to_i

    Time.new(2010,10,10,hour, min, sec)
  end

  def modify(instructions)
    case instructions
    when /Wrong address listed/
      self.ready_at = Time.new(2010, 10, 10, 10, 20)
      self.street = '410 S State St'
      self.zip = 84111
    when /Delayed/
      self.ready_at = Time.new(2010, 10, 10, 9, 5)
    when /Can only be on truck 2/
      self.truck_availability = [2]
    end
  end
end
