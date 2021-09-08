from create_test_input import create_matrix
from collections import defaultdict
def pair_dig_dump(matrix=None):
    if not matrix:
        matrix = create_matrix(5, 5, 5, 10)
    dig_locations = {}
    dump_locations = {}
    # Iterate through the entire matrix, adding digging sites and dumping sites to corresponding dictionary.
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > 0:
                dig_locations[(i,j)] = matrix[i][j]
            elif matrix[i][j] < 0:
                dump_locations[(i,j)] = matrix[i][j]

    def dig_and_dump(dig_location, dump_location):
        dig_count = 0
        while dig_locations[dig_location] and dump_locations[dump_location]:
            dig_locations[dig_location] -= 1
            dump_locations[dump_location] += 1
            dig_count += 1
        return dig_count

    def all_pairs_dig(dig_location, pairs):
        if not dig_locations[dig_location]:
            return pairs
        for dump_location in dump_locations.keys():
            if not dump_locations[dump_location]:
                continue
            dig_count = dig_and_dump(dig_location, dump_location)
            sequence = pairs[-1] + []
            pairs[-1].append(dump_location)
            pairs = all_pairs_dig(dig_location, pairs)
            dig_locations[dig_location] += dig_count
            dump_locations[dump_location] -= dig_count
            pairs.append(sequence)
        pairs = pairs[:-1]
        return pairs

    def all_pairs_all_digs(dig_dump_pairs):
        valid = False
        for dig_location in dig_locations:
            if not dig_locations[dig_location]:
                continue
            valid = True
            pairs = all_pairs_dig(dig_location, [[]]) # get all pairs of digging
            #print('\n',pairs, dig_location)
            for pair in pairs:
                #jprint('pair, dig_location: ', pair, dig_location)
                sequence = {dig_location: dig_dump_pairs[-1][dig_location] for dig_location in dig_dump_pairs[-1]}
                #print('sequence ', sequence)
                dig_counts = []
                for dump_location in pair: # dig
                    dig_counts.append(dig_and_dump(dig_location, dump_location))
                dig_dump_pairs[-1][dig_location] = pair # pair dig locations and dump locations
                #print('dig/dump', dig_dump_pairs)
                dig_dump_pairs = all_pairs_all_digs(dig_dump_pairs) # recurse
                for dump_location, dig_count in zip(pair, dig_counts): # undig
                    dig_locations[dig_location] += dig_count
                    dump_locations[dump_location] -= dig_count
                dig_dump_pairs.append(sequence)
        if valid:
            dig_dump_pairs = dig_dump_pairs[:-1]
        return dig_dump_pairs

    return all_pairs_all_digs([{}])

def level(dig_locations, dump_locations, dig_dump_pairs):
    def dig_and_dump(dig_location, dump_location):
        while dig_locations[dig_location] and dump_locations[dump_location]:
            dig_locations[dig_location] -= 1
            dump_locations[dump_location] += 1

    for dig_location in dig_dump_pairs:
        for dump_location in dig_dump_pairs[dig_location]:
            dig_and_dump(dig_location, dump_location)

import unittest
class Test(unittest.TestCase):
    def level_test(self):
        matrix = create_matrix(5, 5, 5, 10)
        dig_locations = {}
        dump_locations = {}
    
        # Iterate through the entire matrix, adding digging sites and dumping sites to corresponding dictionary.
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] > 0:
                    dig_locations[(i,j)] = matrix[i][j]
                elif matrix[i][j] < 0:
                    dump_locations[(i,j)] = matrix[i][j]

        dig_dump_pairs_permutations = pair_dig_dump([[matrix[i][j] for j in range(len(matrix[i]))] for i in range(len(matrix))])

        # Assert that all dig locations are accounted for.
        for dig_dump_pairs in dig_dump_pairs_permutations:
            for dig_location in dig_locations:
                self.assertTrue(dig_location in dig_dump_pairs)

            dumps_in_pairs = {dump_location for dig_location in dig_dump_pairs for dump_location in dig_dump_pairs[dig_location]}
            for dump_location in dump_locations:
                self.assertTrue(dump_location in dumps_in_pairs)

        # Assert 
                

    number_of_tests = 5
    def test(self):
        #self.test_level()
        for _ in range(self.number_of_tests):
           self.level_test()
"""
matrix = [[4, -4, -1, 0, -3], [0, 0, 0, 0, 0], [0, 0, -1, 0, 0], [0, 0, 2, 0, 0], [0, 1, 0, 0, 2]]
#matrix = [[4, -4, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, -4, 0, 0], [0, 0, 0, 0, 0], [0, 4, 0, 0, 0]]
pair_dig_dump(matrix)
"""
            
