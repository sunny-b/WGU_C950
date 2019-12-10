import os
from datetime import timedelta

from package_delivery_system import PackageDeliverySystem

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

(total_distance, packages_hash, packages) = PackageDeliverySystem.run()

clear()

print('This is the WGU Package Delivery System')
print('All packages were delivered in {} miles'.format(total_distance))

while True:
    print()
    command = input("""\
Command Menu:
   id - look an individual package ID
   time - view delivery status of all packages for a specific time
   distance - display total distance the trucks traveled
   clear - clear screen
   exit - exit program
   Please enter a command: """)

    if command == 'id':
        package_id = input('Please enter a package ID to lookup: ')
        package = packages_hash.find(int(package_id))

        time_string = input('Please enter a timestamp with HH:MM:SS format: ')
        (hour, minute, sec) = time_string.split(':')
        timestamp = timedelta(hours=int(hour), minutes=int(minute), seconds=int(sec))

        print(package.report(timestamp))
    
    elif command == 'time':
        time_string = input('Please enter a timestamp in HH:MM:SS format: ')
        (hour, minute, sec) = time_string.split(':')
        timestamp = timedelta(hours=int(hour), minutes=int(minute), seconds=int(sec))

        for package in packages:
            print(package.inline_report(timestamp))
            
    elif command == 'distance':
        print('Total Distance: {} miles'.format(total_distance))

    elif command == 'clear':
        clear()
    elif command == 'exit':
        exit()
    else:
        print('Invalid command. Please try again.')
