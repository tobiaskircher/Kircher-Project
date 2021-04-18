#finds solution to rubiks cube scramble
#pip instal rubik_solver

from rubik_solver import utils

def run(cube):
    
    solution = utils.solve(cube, "Kociemba")
    print(solution)

    return solution

#cube = 'yyyyyyyyyrrrbbbbbbgggrrrrrroooggggggbbboooooowwwwwwwww'
#run(cube)
#y up, b left, r front, g right, o back, w down
