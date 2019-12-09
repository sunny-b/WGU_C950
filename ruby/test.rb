require_relative 'main'

test_runs = []

result = PackageDeliveryService.run
puts "Result: #{result}"
