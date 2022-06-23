#In button functions at end of solve

        ###TESTING SKIP
        '''game_state.cube = "wogwywyrgrgbgbobroryogrryybybwwgbrryowgooygyobowgwbwbr"
        game_state.state = "solve_solution_screen"
        game_state.solution = solution_generator.run(game_state.cube)
        game_state.solution.insert(0," ")
        game_state.move_counter = 0
        game_state.space_being_pressed = True
        game_state.solving_cube = Virtual_Cube()
        for i in list(reversed(game_state.solution)):
            i = str(i)
            if len(i) > 1:
                if i[1] == "'":
                    game_state.solving_cube.move(i[0])
                elif i[1] == "2":
                    game_state.solving_cube.move(i[0])
                    game_state.solving_cube.move(i[0])       
            elif i != " ":
                game_state.solving_cube.move(i,-1)'''

        ###TESTING SKIP END
