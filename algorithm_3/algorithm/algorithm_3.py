from .distance import euclidean_distance
from collections import defaultdict

def dig_dump(matrix, dig_locations, dump_locations, dig_location, dump_location):
    # Dig and dump between pair until one location is level.

    count = 0
    while dig_locations[dig_location] and dump_locations[dump_location]:

        count += 1
        dig_locations[dig_location] -= 1
        dump_locations[dump_location] += 1

        dig_y, dig_x = dig_location
        dump_y, dump_x = dump_location

        matrix[dig_y][dig_x] -= 1
        matrix[dump_y][dump_x] += 1
    return count

def find_largest_difference(dig_locations, dump_locations):
    # Pair the dig annd dump pairs which seem like the best choice. (Greedy component)
    # Return dig and dump pairs which have the largest distance difference between its closest dump location and its next closest dump location.
    # If the closest dump location to chosen dig location is paired off with another dig location, then the overall pathing distance will be greater.

    # TODO: Use dynamic programming.

    # Get the distances between every dig and dump pair.
    distance_matrix = []
    for dig_location in dig_locations:
        if not dig_locations[dig_location]:
            continue
        distance_matrix.append(sorted([(euclidean_distance(dig_location, dump_location), dig_location, dump_location) for dump_location in dump_locations if dump_locations[dump_location]]))

    # Get the dig locations which are the farthest apart between their closest dump location and their next closest dump location.
    # TODO: Account for edge case when all largest distance difference variables are the same.
    #       Solution is to recalculate largest_difference_list where the closest path distance is subtracted by a path distance with a value other then the next closest path distance.
    largest_differences_list = []
    for dig_location_distances in distance_matrix:
        if len(dig_location_distances) == 1:
            largest_differences_list.append((0, dig_location_distances[0][1], dig_location_distances[0][2]))
        else:
            largest_differences_list.append((dig_location_distances[1][0] - dig_location_distances[0][0], dig_location_distances[0][1], dig_location_distances[0][2]))
    largest_differences_list.sort()

    return largest_differences_list[-1]

def level_ground(matrix):
    # Pair digging and dumping locations to level a given matrix using a greedy approach.

    # Holds dig or dump coordinates  and their elevation.
    dig_locations = {}
    dump_locations = {}
    # Pairs dig and dump location and specifies how many actions must be completed in both locations.
    dig_dump_pairs = defaultdict(list)

    # Iterate through the entire matrix, adding digging sites and dumping sites to corresponding dictionary.
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > 0:
                dig_locations[(i,j)] = matrix[i][j]
            elif matrix[i][j] < 0:
                dump_locations[(i,j)] = matrix[i][j]

    # Check if the sum of dig location values and dump location values is within an acceptable margin of zero.
    if sum(dig_locations.values()) + sum(dump_locations.values()):
        raise ValueError('Sum of locations must be zero')

    while sum(dig_locations.values()) and sum(dump_locations.values()):
        # Pair dig and dump locations until all locations are level.
        distance, dig_location, dump_location = find_largest_difference(dig_locations, dump_locations) # Greedy choice
        number_of_actions = dig_dump(matrix, dig_locations, dump_locations, dig_location, dump_location)
        dig_dump_pairs[dig_location].append((dump_location, number_of_actions)) # Pair

    return matrix, dig_dump_pairs
