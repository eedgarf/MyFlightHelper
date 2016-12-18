class FlightPathManager:

    def __init__(self):
        self.flight_object_list = []

    def add_flight_object(self, flight_record_object):
        self.flight_object_list.append(flight_record_object)

    def get_flight_price(self, fly_from, fly_to, fly_on):
        price = 0
        for flight in self.flight_object_list:
            if flight.get_fly_from() == fly_from and flight.get_fly_to() == fly_to and flight.get_fly_on() == fly_on:
                price = flight.get_fly_price()
                break
        return price

    def sort_flight_objects_by_price(self):
        self.flight_object_list = sorted(self.flight_object_list, key=lambda x: x.get_fly_price(), reverse=True)
        return self.flight_object_list[0]
