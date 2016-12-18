from datetime import datetime


class FlightPath:
    def __init__(self, flight_record_data):
        self.TravelDate = flight_record_data["TravelDate"]
        self.Airlines = flight_record_data["Airlines"]
        self.FromAirport = flight_record_data["FromAirport"]
        self.ToAirport = flight_record_data["ToAirport"]
        self.OutBoundTime = flight_record_data["OutboundTime"]
        self.InboundTime = flight_record_data["InboundTime"]
        self.TravelPrice = flight_record_data["Price"]

    def get_fly_from(self):
        return self.FromAirport

    def get_fly_to(self):
        return self.ToAirport

    def get_fly_on(self):
        date = datetime.strptime(self.TravelDate, "%d-%m-%Y")
        return date.strftime("%Y-%m-%d") # revert from momondo format to the typical one

    def get_flight_date_from_to(self):
        request_data = {"TravelDate": self.TravelDate, "FromAirport": self.FromAirport, "ToAirport": self.ToAirport}
        return request_data

    def get_fly_price(self):
        return self.TravelPrice
