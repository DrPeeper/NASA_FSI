matrix_length = 5
matrix_height = 5
number_of_digs = 10
number_of_locations = 5

import random
def create_matrix(matrix_length, matrix_height, number_of_locations, number_of_digs):
    # Number of locations cannot exceed (matrix_length * matrix_height)/2
    if number_of_locations > int((matrix_length * matrix_height)/2):
        return None

    # Number of digs cannot exceed number of dig locations.
    if number_of_locations > number_of_digs:
        return None

    matrix = [[0 for _ in range(matrix_length)] for _ in range(matrix_height)]        
    dig_locations = set()
    dump_locations = set()

    # Choose locations.
    for _ in range(number_of_locations):
        def choose_index():
            return (random.randint(0, matrix_height - 1), random.randint(0, matrix_length - 1))
        # Choose dig location.
        dig_location = choose_index()
        while dig_location in dig_locations or dig_location in dump_locations:
            dig_location = choose_index()
        dig_locations.add(dig_location)

        # Choose dump location.
        dump_location = choose_index()
        while dump_location in dump_locations or dump_location in dig_locations:
            dump_location = choose_index()
        dump_locations.add(dump_location)

    # Change dig location and dump location values.
    for _ in range(number_of_digs):
        dig_location = random.choice(list(dig_locations))
        matrix[dig_location[0]][dig_location[1]] += 1

        dump_location = random.choice(list(dump_locations))
        matrix[dump_location[0]][dump_location[1]] -= 1
    return matrix
