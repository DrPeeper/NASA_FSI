# Unit Tests
from create_test_input import create_matrix
from brute_force.brute_force import pair_dig_dump
import unittest
import sys
sys.path.append('..')
from algorithm import level_ground, distance_between_pairs_comparison, distance_between_pairs, distance_difference

class Test(unittest.TestCase):
    matrix_length = 5
    matrix_height = 5
    number_of_digs = 10
    number_of_locations = 3

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
        
        # Check that matrix is all zeroes.
        for row in matrix:
            for column in row:
                self.assertEqual(column, 0)

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

    def redundency_and_action_test(self):
        # Test pairing redundency.
        # Test the correct number of actions are required.
        actions_truly_required = - 1 * sum(self.dump_locations.values()) + sum(self.dig_locations.values())
        actions_solution_required = 0
        for dig_location in self.dig_dump_pairs:
            for dump_location, actions_required in self.dig_dump_pairs[dig_location]:
                # Assert that the level of niether pair is zero
                self.assertNotEqual(0, self.dig_locations[dig_location])
                self.assertNotEqual(0, self.dump_locations[dump_location])

                # Ensure that digging or dumping is required
                self.assertNotEqual(0, actions_required)

                # Level
                for _ in range(actions_required):
                    self.dig_locations[dig_location] += 1
                    self.dump_locations[dump_location] -= 1

                # Sum actions that the solution required.
                actions_solution_required += actions_required * 2

        # Assert instructions create a level matrix
        self.assertEqual(0, sum(self.dump_locations.values()) + sum(self.dig_locations.values()))

        # Test redundency in actions required
        self.assertEqual(actions_truly_required, actions_solution_required)

    def shortest_path(self):
        # Test that the given dig dump pairs provides the shortest total pathing distance.
        all_pairs_all_digs = pair_dig_dump([[self.original_matrix[i][j] for j in range(len(self.original_matrix[i]))] for i in range(len(self.original_matrix))])

        shortest_dig_dump_pairs, _ = distance_between_pairs_comparison(all_pairs_all_digs[0], all_pairs_all_digs[1])
        self.assertIsNotNone(shortest_dig_dump_pairs)
        for dig_dump_pairs in all_pairs_all_digs[2:]:
            shortest_dig_dump_pairs, _ = distance_between_pairs_comparison(shortest_dig_dump_pairs, dig_dump_pairs)
            self.assertIsNotNone(shortest_dig_dump_pairs)

        print(shortest_dig_dump_pairs, '\n', self.dig_dump_pairs)
        distance_1, distance_2 = distance_between_pairs(shortest_dig_dump_pairs, self.dig_dump_pairs)
        differences = distance_difference(self.dig_dump_pairs)
        print('-')
        for a in differences:
            print(a)
        print('-')
        print(distance_1, distance_2)
        if distance_1 == distance_2:
            return
        shortest_dig_dump_pairs, _ = distance_between_pairs_comparison(self.dig_dump_pairs, shortest_dig_dump_pairs)
        self.assertEqual(self.dig_dump_pairs.keys(), shortest_dig_dump_pairs.keys())
        for dig_location in self.dig_dump_pairs:
            shortest_dig_dump_pairs[dig_location].sort()
            self.dig_dump_pairs[dig_location].sort()
            self.assertEqual(shortest_dig_dump_pairs[dig_location], self.dig_dump_pairs[dig_location])
        #self.assertEqual(shortest_dig_dump_pairs, self.dig_dump_pairs)

    number_of_tests = 1000
    def test(self):
        for _ in range(self.number_of_tests):
            self.init()
            self.level_test()
            self.completion_test()
            self.redundency_and_action_test()
            self.shortest_path()
