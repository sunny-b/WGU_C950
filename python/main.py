import os
from datetime import timedelta

from package_delivery_system import PackageDeliverySystem

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

(total_distance, packages_hash, packages) = PackageDeliverySystem.run()

print('This is the WGU Package Delivery System')
print('All packages were delivered in {} miles'.format(total_distance))

clear()

while True:
    command = input("Type 'id' to look an individual package ID or \n \
'time' to view delivery status for a specific time or \n \
'exit' to end: ")

    if command == 'id':
        package_id = input('Please enter a package ID to lookup: ')
        package = packages_hash.find(int(package_id))
        print(package.report())
        print()
    
    elif command == 'time':
        time_string = input('Please enter a timestamp with (HH:MM:SS) format: ')
        (hour, minute, sec) = time_string.split(':')
        timestamp = timedelta(hours=int(hour), minutes=int(minute), seconds=int(sec))

        for package in packages:
            print(package.report(timestamp))

        print()


    elif command == 'exit':
        exit()
    else:
        print('Invalid command. Please try again.')
        print()
