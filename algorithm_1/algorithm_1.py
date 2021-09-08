from create_test_input import create_matrix
from distance import euclidean_distance, distance_between_pairs
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

    for dig_location in dig_locations:
        dig_completed = False

        # Get distance from dig_location to all other dump locations.
        distances_and_dump_locations = defaultdict(list)
        for dump_location  in dump_locations:
            distances_and_dump_locations[euclidean_distance(dig_location, dump_location)].append(dump_location)

        distances = list(distances_and_dump_locations.keys())
        distances.sort()
        for distance in distances:
            for dump_location in distances_and_dump_locations[distance]:
                # Pair dig and dump location.
                dig_dump_pairs[dig_location].append(dump_location)
                while dig_locations[dig_location] and dump_locations[dump_location]:
                    # Perform dig.
                    dig_locations[dig_location] -= 1
                    matrix[dig_location[0]][dig_location[1]] -= 1
                    # Perfom dump.
                    dump_locations[dump_location] += 1
                    matrix[dump_location[0]][dump_location[1]] += 1

                if not dump_locations[dump_location]:
                    del dump_locations[dump_location]
                if not dig_locations[dig_location]:
                    dig_completed = True
                    break

            if dig_completed:
                break
        if dig_completed:
            continue

    return matrix, dig_dump_pairs

import unittest
import json
from brute_force import pair_dig_dump
class Test(unittest.TestCase):
    matrix_length = 5
    matrix_height = 5
    number_of_digs = 10
    number_of_locations = 5

    def shortest_distance_test(self, dig_dump_pairs, matrix):
        dig_dump_pairs_permutations = pair_dig_dump(matrix)
        shortest_distance = distance_between_pairs(dig_dump_pairs_permutations[0])
        for dig_dump_pairs in dig_dump_pairs_permutations[1:]:
            test_distance = distance_between_pairs(dig_dump_pairs)
            shortest_distance = shortest_distance if shortest_distance < test_distance else test_distance
        self.assertEqual(shortest_distance, distance_between_pairs(dig_dump_pairs))
    
    def level_test(self):
        print('----------------------------------------------------------------------')
        matrix = create_matrix(self.matrix_length, self.matrix_height, self.number_of_locations, self.number_of_digs)
        original_matrix = [[matrix[i][j] for j in range(len(matrix[i]))] for i in range(len(matrix))]
        # Get variables for testing
        dig_locations = {}
        dump_locations = {}
    
        # Iterate through the entire matrix, adding digging sites and dumping sites to corresponding dictionary.
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] > 0:
                    dig_locations[(i,j)] = matrix[i][j]
                elif matrix[i][j] < 0:
                    dump_locations[(i,j)] = matrix[i][j]
                    
        print(f'Testing leveling algorithm on the following matrix:\n{matrix}\n')
        matrix, dig_dump_pairs = level_ground(matrix)
        print(f'Leveling algorithm matrix output (should all be zeros):\n{matrix}\n\nDig location and Dump location pairs:')
        for dig_location in dig_dump_pairs.keys():
            print(f'{dig_location}: ', end='')
            for dump_location in dig_dump_pairs[dig_location]:
                print(f'{dump_location} ', end='')
            print()

        # Check that matrix is all zeroes.
        for row in matrix:
            for column in row:
                self.assertEqual(column, 0)

        # Check that all dig locations and dump locations are found in dig/dump pairs.
        for dig_location in dig_locations:
            self.assertTrue(dig_location in dig_dump_pairs)

        dig_dump_pairs_dump_locations = {dump_location for dump_locations in dig_dump_pairs.values() for dump_location in dump_locations}     

        for dump_location in dump_locations:
            self.assertTrue(dump_location in dig_dump_pairs_dump_locations)
        """
        # Check that dig locations are paired with closest dump locations.
        dump_locations_copy = {dump_location for dump_location in dump_locations}

        for dig_location in dig_locations:
            for dump_location in dig_dump_pairs[dig_location]: # for each dump location paired to dig location
                self.assertNotEqual(dump_locations[dump_location], 0)
                
                while dig_locations[dig_location] and dump_locations[dump_location]: # dig/dump
                    dig_locations[dig_location] -= 1
                    dump_locations[dump_location] += 1
                    
                for dump_location_to_compare in dump_locations_copy: # compare chosen dump location distance to all other dump location distances
                    self.assertLessEqual(euclidean_distance(dig_location, dump_location), euclidean_distance(dig_location, dump_location_to_compare))
                if not dump_locations[dump_location]: # if dump location is level, don't use it anymore
                    dump_locations_copy.remove(dump_location)
        """
        self.shortest_distance_test(dig_dump_pairs, original_matrix)

    number_of_tests = 5
    def test(self):
        for _ in range(self.number_of_tests):
            self.level_test()

