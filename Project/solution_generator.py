#SOLUTION GENERATOR

#import required library
from rubik_solver import utils

#return solution to rubik's cube using Kociemba
def run(cube):
    solution = utils.solve(cube, "Kociemba")
    return solution
