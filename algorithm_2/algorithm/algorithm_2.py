from .distance import euclidean_distance, distance_between_pairs
from collections import defaultdict

def level_ground(matrix):
    dig_locations = {}
    dump_locations = {}
    dig_dump_pairs = defaultdict(list)
    
    # Iterate through the entire matrix, adding digging sites and dumping sites to corresponding dictionary.
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > 0:
                dig_locations[(i,j)] = matrix[i][j]
            elif matrix[i][j] < 0:
                dump_locations[(i,j)] = matrix[i][j]

    def dig_dump(dig_location, dump_location):
        while dig_locations[dig_location] and dump_locations[dump_location]:
            dig_locations[dig_location] -= 1
            dump_locations[dump_location] += 1

            dig_y, dig_x = dig_location
            dump_y, dump_x = dump_location

            matrix[dig_y][dig_x] -= 1
            matrix[dump_y][dump_x] += 1

    # get distance of every dig location to every dump location
    distances = defaultdict(list)
    #dump_location_list = dump_locations.values()
    for dig_location in dig_locations:
        for dump_location in dump_locations:
            dig_dump_actions = dig_locations[dig_location] if dig_locations[dig_location] < dump_locations[dump_location] * -1 else dump_locations[dump_location] * -1
            distances[euclidean_distance(dig_location, dump_location) * dig_dump_actions].append((dig_location, dump_location))

    count = 0
    smallest_distance = list(distances.keys())
    smallest_distance.sort()

    for distance in smallest_distance:
        for dig_location, dump_location in distances[distance]:
            if dig_locations[dig_location] and dump_locations[dump_location]:
                # Count required actions to be performed between the two sites.
                dig_dump_actions = dig_locations[dig_location] if dig_locations[dig_location] < dump_locations[dump_location] * -1 else dump_locations[dump_location] * -1
                # Perform actions.
                dig_dump(dig_location, dump_location)
                # Pair.
                dig_dump_pairs[dig_location].append((dump_location, dig_dump_actions))

    return matrix, dig_dump_pairs
