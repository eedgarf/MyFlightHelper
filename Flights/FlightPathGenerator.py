from Flights.FlightBrowser import FlightBrowser
from Flights.FlightPathManager import FlightPathManager
from datetime import datetime, timedelta


def get_upcoming_multitravel_date(base_date):  # TODO: impelement real date span functionaly for multi travel
    date = datetime.strptime(base_date, "%Y-%m-%d")
    date = date + timedelta(days=3)
    return date.strftime("%Y-%m-%d")


def get_upcoming_single_travel_date(base_date):
    date = datetime.strptime(base_date, "%Y-%m-%d")
    date = date + timedelta(days=1)
    return date.strftime("%Y-%m-%d")


class FlightPathGenerator:

    def __init__(self):
        self.path_permutations = None
        self.fp_manager = FlightPathManager()
        self.updated_flight_permutation = []

    def generate_multipermutation_flight_objects(self, permutations, flight_start_date): #generate flight objects for all the permutations
        self.path_permutations = permutations
        for path in self.path_permutations:
            counter = 0
            fdate = flight_start_date
            while counter < len(path) - 1: # Protect ourselves against overflow as we access n, n+1 elements at a given
                                           # time. No need to go to upper end and get out range error below...
                from_destination = path[counter]
                to_destination = path[counter + 1]
                if counter != 0:          # If counter != 0 we somewhere at n+1, n+2 element range. Time to update trave date for the hop
                    fdate = get_upcoming_multitravel_date(fdate)
                fbrowser = FlightBrowser(from_destination, to_destination, fdate) #Init flight-data request browser
                self.fp_manager.add_flight_object(fbrowser.execute_request()) #Add flight-object of type FlightPath to a manager class
                counter += 1

    def generate_prices_for_paths(self, flight_start_date): # variation of gen_flight_objects algorhithm to get the price for a path permutation
        for path in self.path_permutations:
            price = 0
            counter = 0
            fdate = flight_start_date
            while counter < len(path) - 1:
                from_destination = path[counter]
                to_destination = path[counter + 1]
                if counter != 0:
                    fdate = get_upcoming_multitravel_date(fdate)
                price += int(self.fp_manager.get_flight_price(from_destination, to_destination, fdate))
                if counter + 1 == len(path) - 1:  #If we traversed all the elements in n, n+1 fashion, post-pend the price to path
                    self.updated_flight_permutation.append(path + (price,))
                counter += 1

    def generate_flight_objects(self, fly_from, fly_to, fly_on, day_range_to_check): #generate f objs based on single dest with diff dates
        iterGuard = 0  # we start updating the fly_on date if it is != 0
        while day_range_to_check != 0:
            if iterGuard != 0:
                fly_on = get_upcoming_single_travel_date(fly_on)
            flight_browser = FlightBrowser(fly_from, fly_to, fly_on)
            self.fp_manager.add_flight_object(flight_browser.execute_request())
            day_range_to_check -= 1
            iterGuard += 1
        cheapest_flight = self.fp_manager.sort_flight_objects_by_price()
        return cheapest_flight

    def get_cheapest_travel_path(self):
        sorted_permutations = sorted(self.updated_flight_permutation, key=lambda x: x[-1], reverse=True)
        return sorted_permutations[0]
