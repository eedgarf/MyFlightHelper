from itertools import permutations


def get_permutations_for_home_return(raw_permutation, start_airport): # We take any permutation with perm[0] matching
    #  start dest and prepend start(end) destination to the end
    needed_permutations = []
    for permutation in list(raw_permutation):
        if permutation[0] == start_airport:
            needed_permutations.append(permutation + (start_airport,))
    return needed_permutations


def get_simple_permutation_list(raw_permutation, start_airport): # We take any permutation with perm[0] matching
    # start dest
    needed_permutations = []
    for permutation in list(raw_permutation):
        if permutation[0] == start_airport:
            needed_permutations.append(permutation)
    return needed_permutations


def create_list_of_travel_variations(destination_list, start_dest, return_home=True):
    raw_permutations = permutations(destination_list)

    if return_home:
        result_permutations = get_permutations_for_home_return(raw_permutations, start_dest)
    else:
        result_permutations = get_simple_permutation_list(raw_permutations, start_dest)

    return result_permutations
