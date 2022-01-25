#finds solution to rubiks cube scramble
#pip instal rubik_solver

import rubik_solver

def run(cube):
    
    solution = rubik_solver.utils.solve(cube, "Kociemba")
    #print(solution)

    return solution

#cube = 'yyyyyyyyyrrrbbbbbbgggrrrrrroooggggggbbboooooowwwwwwwww'
#run(cube)
#y up, b left, r front, g right, o back, w down
