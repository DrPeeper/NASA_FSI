from .distance import euclidean_distance
from collections import defaultdict

def level_ground(matrix=None):
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

    def find_largest_difference():
        # Return dig and dump pairs which make largest distance difference between the largest distance and smallest distance.

        distance_matrix = []
        for dig_location in dig_locations:
            if not dig_locations[dig_location]:
                continue
            distance_matrix.append(sorted([(euclidean_distance(dig_location, dump_location), dig_location, dump_location) for dump_location in dump_locations if dump_locations[dump_location]]))

        largest_differences_list = []
        for dig_location_distances in distance_matrix:
            if len(dig_location_distances) == 1:
                largest_differences_list.append((0, dig_location_distances[0][1], dig_location_distances[0][2]))
            else:
                index = 1
                for distance, _, _ in dig_location_distances[1:]:
                    if distance == dig_location_distances[0][0]:
                        index+=1
                    else:
                        break
                if index >= len(dig_location_distances):
                    index -= 1
                largest_differences_list.append((dig_location_distances[index][0] - dig_location_distances[0][0], dig_location_distances[0][1], dig_location_distances[0][2]))
        largest_differences_list.sort()
        return largest_differences_list[-1]

    while sum(dig_locations.values()) and sum(dump_locations.values()):
        distance, dig_location, dump_location = find_largest_difference()
        actions = dig_dump(dig_location, dump_location)
        print(distance, dig_location, dump_location, actions)
        dig_dump_pairs[dig_location].append((dump_location, actions))

    return matrix, dig_dump_pairs
