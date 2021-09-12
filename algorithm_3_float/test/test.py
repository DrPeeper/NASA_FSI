# Unit Tests
from create_test_input import create_matrix
import unittest
import sys
sys.path.append('..')
from algorithm import level_ground, distance_between_pairs_comparison, distance_between_pairs, distance_difference
import math

class Test(unittest.TestCase):
    matrix_length = 5
    matrix_height = 5
    number_of_digs = 10
    number_of_locations = 5

    threshold = .09

    def init(self):
        self.matrix = create_matrix(self.matrix_length, self.matrix_height, self.number_of_locations, self.number_of_digs)
        self.original_matrix = [[self.matrix[i][j] for j in range(len(self.matrix[i]))] for i in range(len(self.matrix))]

        self.dig_locations = {}
        self.dump_locations = {}
        self.get_locations()
        self.dig_dump_pairs = None

    def get_locations(self):
        # Iterate through the entire matrix, adding digging sites and dumping sites to corresponding dictionary.
        for i in range(len(self.original_matrix)):
            for j in range(len(self.original_matrix[i])):
                if self.original_matrix[i][j] > 0:
                    self.dig_locations[(i,j)] = self.original_matrix[i][j]
                elif self.original_matrix[i][j] < 0:
                    self.dump_locations[(i,j)] = self.original_matrix[i][j]

    def level_test(self):
        print('----------------------------------------------------------------------')
        print(f'Testing leveling algorithm on the following matrix:\n{self.matrix}\n')
        matrix, self.dig_dump_pairs = level_ground(self.matrix)

        
        print(f'Leveling algorithm matrix output (should all be zeros):\n{matrix}\n\nDig location and Dump location pairs:\n')
        
        # Check that matrix are all level.
        unlevel_location_flag = False
        for row in matrix:
            for column in row:
                if column != 0 and not unlevel_location_flag:
                    unlevel_location_flag = True
                    continue
                self.assertLessEqual(abs(column), self.threshold)

        # Print out instructions
        for dig_location in self.dig_dump_pairs.keys():
            print(f'Dig Location: {dig_location}: ')
            for dump_location, actions_required in self.dig_dump_pairs[dig_location]:
                print(f'Dump Location{dump_location}; Actions Required: {actions_required}')
            print()

    def completion_test(self):
        # Check that all dig locations and dump locations are found in dig/dump pairs.
        for dig_location in self.dig_locations:
            self.assertTrue(dig_location in self.dig_dump_pairs)

        dig_dump_pairs_dump_locations = {dump_location[0] for dump_locations in self.dig_dump_pairs.values() for dump_location in dump_locations}     

        for dump_location in self.dump_locations:
            self.assertTrue(dump_location in dig_dump_pairs_dump_locations)

    def redundency_and_action_completion_test(self):
        # Test that all pairs are necessary.
        # Test that instructions create a level matrix.

        for dig_location in self.dig_dump_pairs:
            for dump_location, actions_required in self.dig_dump_pairs[dig_location]:
                # Test pairing redundency.
                # Assert that the level of niether pair is zero
                self.assertNotEqual(0, self.dig_locations[dig_location])
                self.assertNotEqual(0, self.dump_locations[dump_location])

                # Ensure that solution requires digging or dumping
                self.assertNotEqual(0, actions_required)

                # Level
                self.dig_locations[dig_location] -= actions_required
                self.dump_locations[dump_location] += actions_required

        # Assert instructions create a level matrix except for the one value which holds the excess resources.
        unlevel_location_flag = False
        for locations in [self.dig_locations, self.dump_locations]:
            for location in locations:
                if abs(locations[location]) > self.threshold:
                    if not unlevel_location_flag:
                        unlevel_location_flag = True
                        continue
                self.assertLessEqual(abs(locations[location]), self.threshold)

        self.assertFalse(unlevel_location_flag)

    number_of_tests = 10000
    def test(self):
        average_shortest_solution_distance_ratio = 0
        for _ in range(self.number_of_tests):
            self.init()
            self.level_test()
            self.completion_test()
            self.redundency_and_action_completion_test()

