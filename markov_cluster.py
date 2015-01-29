import numpy as np
import math

EXPANSION_POWER = 2
INFLATION_POWER = 2
ITERATION_COUNT = 100

def normalize(matrix):
    return matrix/np.sum(matrix, axis=0)

def expand(matrix, power):
    return np.linalg.matrix_power(matrix, power)

def inflate(matrix, power):
    for entry in np.nditer(matrix, op_flags=['readwrite']):
        entry[...] = math.pow(entry, power)
    return matrix

def run(matrix):
    np.fill_diagonal(matrix, 1)
    matrix = normalize(matrix)
    for _ in range(ITERATION_COUNT):
        matrix = normalize(inflate(expand(matrix, EXPANSION_POWER), INFLATION_POWER))
    return matrix

'''
transition_matrix = np.matrix([[0,0.97,0.5],[0.2,0,0.5],[0.8,0.03,0]])
final_matrix = run(transition_matrix)
print final_matrix
'''