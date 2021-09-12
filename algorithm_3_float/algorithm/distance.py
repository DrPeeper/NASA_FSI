from math import sqrt
# Find euclidean distance between two points.
def euclidean_distance(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# Find arguemnt which provides the shortest rover pathing.
def distance_between_pairs_comparison(dig_dump_pairs_1, dig_dump_pairs_2):
    if dig_dump_pairs_1.keys() != dig_dump_pairs_2.keys():
        return None
    distance_1 = 0
    distance_2 = 0
    for dig_location in dig_dump_pairs_1:
        for dump_location, actions_required in dig_dump_pairs_1[dig_location]:
            distance_1 += euclidean_distance(dig_location, dump_location) * actions_required
        for dump_location, actions_required in dig_dump_pairs_2[dig_location]:
            distance_2 += euclidean_distance(dig_location, dump_location) * actions_required
    return (dig_dump_pairs_1, distance_1) if distance_1 < distance_2 else (dig_dump_pairs_2, distance_2)

# Return rover pathing distance of two dig dump pairs with all of the same dig locations.
def distance_between_pairs(dig_dump_pairs_1, dig_dump_pairs_2):
    if dig_dump_pairs_1.keys() != dig_dump_pairs_2.keys():
        return None
    distance_1 = 0
    distance_2 = 0
    for dig_location in dig_dump_pairs_1:
        for dump_location, actions_required in dig_dump_pairs_1[dig_location]:
            distance_1 += euclidean_distance(dig_location, dump_location) * actions_required
        for dump_location, actions_required in dig_dump_pairs_2[dig_location]:
            distance_2 += euclidean_distance(dig_location, dump_location) * actions_required
    return distance_1, distance_2

# Find distances between every dig and dump location given a dig dump pair.
def distance_difference(dig_dump_pairs):
    dig_dump_differences = []
    dump_locations = {dump_location for dig_location in dig_dump_pairs for dump_location, _ in dig_dump_pairs[dig_location]}
    for dig_location in dig_dump_pairs:
        dig_dump_differences.append([])
        for dump_location in dump_locations:
            dig_dump_differences[-1].append((dig_location, dump_location, euclidean_distance(dig_location, dump_location)))

    return dig_dump_differences
