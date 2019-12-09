from datetime import timedelta
import re

class Package(object):
    EOD_TIMESTAMP = timedelta(hours=17)
    SPECIAL_PACKAGES = [13, 15, 19]
    DELIVERED = "DELIVERED"
    ON_TRUCK = "ON TRUCK"
    AT_HUB = "AT HUB"

    def __init__(self, identifier, street, city, zipcode, deadline, weight_in_kilos, notes, destination):
        self.identifier = int(identifier)
        self.street = street
        self.city = city
        self.zip = zipcode
        self.deadline = self._convert_to_timestamp(deadline)
        self.weight_in_kilos = weight_in_kilos
        self.notes = notes
        self.destination = destination

        self.delivered_at = None
        self.ready_at = timedelta(hours=8)
        self.left_hub_at = None
        self.on_truck = False
        self.truck_availability = [1, 2]
        self.notes = notes

        self._modify(notes)

    def report(self, time=timedelta(hours=17)):
        report ="""\
                ID: {}
                Destination: {}
                Deadline: {}
                Delivery Status: {}\
                """.format(
                    self.identifier,
                    self.destination.address,
                    self.left_hub_at
                )

       if time > self.delivered_at:
           report += """\
                     Delivered On Time: {}\
                     """

        return 'ID: {}\n \
                Destination: {}\n \
                Left Hub At: {}\n \
                Deadline: {}\n \
                Delivery Status: {}\n \
                Delivered At: {}\n \
                Delivered On Time: {}'.format(
                    self.identifier,
                    self._status(time),
                    self.destination.address,
                    self.left_hub_at,
                    self.deadline,
                    self.delivered_at,
                    self.delivered_at <= self.deadline
                )

    def has_deadline(self):
        return self.deadline != self.EOD_TIMESTAMP

    def is_high_priority(self):
        return self.has_deadline() or self.notes != 'None' or self.identifier in self.SPECIAL_PACKAGES

    def can_be_delivered_by(self, truck):
        return not self.on_truck and truck.identifier in self.truck_availability and truck.current_time >= self.ready_at

    def _status(self, time):
        if time > self.delivered_at:
            return self.DELIVERED
        elif time > self.left_hub_at:
            return self.ON_TRUCK

        return self.AT_HUB

    def _convert_to_timestamp(self, time_string):
        if time_string == 'EOD':
            return self.EOD_TIMESTAMP

        (hour, minute, sec) = time_string.split(':')
        return timedelta(hours=int(hour), minutes=int(minute), seconds=int(sec))

    def _modify(self, notes):
        if re.match('Wrong address listed', notes):
            self.ready_at = timedelta(hours=10, minutes=20)
            self.street = '410 S State St'
            self.zip = 84111
        elif re.match('Delayed', notes):
            self.ready_at = timedelta(hours=9, minutes=5)
        elif re.match('Can only be on truck 2', notes):
            self.truck_availability = [2]
