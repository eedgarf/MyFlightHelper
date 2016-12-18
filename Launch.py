from Flights.FlightPathGenerator import FlightPathGenerator
from Flights.Util import create_list_of_travel_variations

print("Flight helper starting... ")
print("WARNING: currently the manager uses a step of 3 days between any two destinations")

print("\nPossible operation modes: M(Multiple destinations) S(Single destination)")
mode = input("Please choose operation mode (M/S): ")
mode = mode.upper()

if mode == "M":
    destinations = input("\nPlease enter an comma separated list of 3 letter airport abbreviations you would like to travel: ")
    destinations = destinations.upper()  # Protect ourselves from lowercase input
    destinations = destinations.replace(" ", "")  # Remove all spaces
    destinations = destinations.split(sep=",")  # Get an list that can be feed into permutation generator
    start_destination = input("Please enter airport abbreviation matching starting point: ")
    start_destination = start_destination.upper()

    while start_destination not in destinations:
        print("Error: start destination is not in the list of already entered travel destinations")
        start_destination = input("Please re-enter the start destination")
        start_destination = start_destination.upper()

    travel_start_date = input("Enter the date for the initial flight in (Y-m-d) format: ")

    return_home = input("Would you like to end your journey by returning home(Y/N)?: ")
    return_home = return_home.upper()

    if return_home == "Y":
        return_home = True
    elif return_home == "N":
        return_home = False
    else:
        print("Malformed return home input...")
        exit(-1)  # lets do something more interesting/stupid for a change...

    permutations = create_list_of_travel_variations(destinations, start_destination, return_home=return_home)  # get all
    # permutations for given travel criteria

    fpg = FlightPathGenerator()  # initialize Generator insantance with the list of destinations
    fpg.generate_multipermutation_flight_objects(permutations ,travel_start_date)  # generate data populated flight objects for all permutationn
    fpg.generate_prices_for_paths(travel_start_date)  # calculate the price for every travel path variation/permutation
    print(fpg.get_cheapest_travel_path())  # prints the cheapest route to visit x, y, z airports :)
elif mode == "S":
    travel_from = input("\nPlease enter start airport (3 letters): ")
    travel_from = travel_from.upper()
    travel_to = input("Please enter destination airport (3 letters): ")
    travel_to = travel_to.upper()
    travel_on = input("Please enter start date from which to check (Y-m-d): ")
    span = input("Please enter number of days to check (0-x): ")
    span = int(span)

    fpg = FlightPathGenerator()
    flight_data = fpg.generate_flight_objects(travel_from, travel_to, travel_on, span)
    print("\nChepest flight found on: {0}".format(flight_data.get_fly_on()))
    print("Cheapest flight price is: {0} GBP".format(flight_data.get_fly_price()))


