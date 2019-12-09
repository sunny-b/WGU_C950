import os
from datetime import timedelta

from package_delivery_system import PackageDeliverySystem

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

(total_distance, packages_hash, packages) = PackageDeliverySystem.run()

clear()

print('This is the WGU Package Delivery System')
print('All packages were delivered in {} miles'.format(total_distance))
print()

while True:
    command = input(
            "Command Menu: \n \
               id - look an individual package ID \n \
               time - view delivery status of all packages for a specific time \n \
               clear - clear screen \n \
               exit - exit program \n \
               Please enter a command: "
            )

    if command == 'id':
        package_id = input('Please enter a package ID to lookup: ')
        package = packages_hash.find(int(package_id))

        time_string = input('Please enter a timestamp with HH:MM:SS format: ')
        (hour, minute, sec) = time_string.split(':')
        timestamp = timedelta(hours=int(hour), minutes=int(minute), seconds=int(sec))

        print(package.report(timestamp))
        print()
    
    elif command == 'time':
        time_string = input('Please enter a timestamp in HH:MM:SS format: ')
        (hour, minute, sec) = time_string.split(':')
        timestamp = timedelta(hours=int(hour), minutes=int(minute), seconds=int(sec))

        for package in packages:
            print(package.report(timestamp))

        print()

    elif command == 'clear':
        clear()
    elif command == 'exit':
        exit()
    else:
        print('Invalid command. Please try again.')
        print()
