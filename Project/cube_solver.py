import pygame, time, random
import numpy as np
import scan_face, solution_generator

#Virtual Cube

class Piece():
    def __init__(self, position, colours):
        #[0,0,0] being centre piece (does not exist, in middle of cube)
        self.position = position
        #[clr facing x dir, clr facing y dir, clr facing z dir]
        self.colours = colours

        colour_count = 0
        for colour in colours:
            if colour != None:
                colour_count+=1
                
        if colour_count == 1:
            self.type = "center"
        elif colour_count == 2:
            self.type = "edge"
        elif colour_count == 3:
            self.type = "corner"

    def __str__(self):
        line1 = "Position: " + str(self.position)
        line2 = "Colours: " + str(self.colours)
        return line1 + "\n" + line2
        
class Virtual_Cube():
    def __init__(self):
        #initiate cube pieces
        #orientation: yellow facing up, red facing towards you
        
        #centre pieces
        #eg. y = yellow center piece
        self.y = Piece([0,1,0],[None,"Y",None])
        self.b = Piece([-1,0,0],["B",None,None])
        self.r = Piece([0,0,1],[None,None,"R"])
        self.g = Piece([1,0,0],["G",None,None])
        self.o = Piece([0,0,-1],[None,None,"O"])
        self.w = Piece([0,-1,0],[None,"W",None])

        #edge pieces
        #eg. yb = yellow + blue edge piece
        self.yb = Piece([-1,1,0],["B","Y",None])
        self.yr = Piece([0,1,1],[None,"Y","R"])
        self.yg = Piece([1,1,0],["G","Y",None])
        self.yo = Piece([0,1,-1],[None,"Y","O"])
        self.wb = Piece([-1,-1,0],["B","W",None])
        self.wr = Piece([0,-1,1],[None,"W","R"])
        self.wg = Piece([1,-1,0],["G","W",None])
        self.wo = Piece([0,-1,-1],[None,"W","O"])
        self.br = Piece([-1,0,1],["B",None,"R"])
        self.bo = Piece([-1,0,-1],["B",None,"O"])
        self.gr = Piece([1,0,1],["G",None,"R"])
        self.go = Piece([1,0,-1],["G",None,"O"])

        #corner pieces
        #eg ybr = yellow+blue+red corner piece
        self.ybr = Piece([-1,1,1],["B","Y","R"])
        self.ybo = Piece([-1,1,-1],["B","Y","O"])
        self.ygo = Piece([1,1,-1],["G","Y","O"])
        self.ygr = Piece([1,1,1],["G","Y","R"])
        self.wbr = Piece([-1,-1,1],["B","W","R"])
        self.wbo = Piece([-1,-1,-1],["B","W","O"])
        self.wgr = Piece([1,-1,1],["G","W","R"])
        self.wgo = Piece([1,-1,-1],["G","W","O"])

        self.pieces = [
            self.y, self.b, self.r, self.g, self.o, self.w,
            self.yb, self.yr, self.yg, self.yo,
            self.wb, self.wr, self.wg, self.wo,
            self.br, self.bo, self.gr, self.go,
            self.ybr, self.ybo, self.ygr, self.ygo,
            self.wbr, self.wbo, self.wgr, self.wgo
        ]

        #variables
        self.axes= {"x":0,
               "y":1,
               "z":2
               }
        #each rotation on an axis affects another axis of the pieces value
        #for example r affects all pieces with x=1, but it changes their y and z values
        self.axis_affects = {"x":["y","z"],
                             "y":["z","x"],
                             "z":["x","y"]
                             }

    def move(self, move, direction=None):
        if direction == None: direction = 1
        else: direction = -1

        x_axis_rotations = ["L", "M", "R"]
        y_axis_rotations = ["D", None, "U"]
        z_axis_rotations = ["B", None, "F"]

        if move in x_axis_rotations:
            axis_of_rotation = "x"
            pieces_to_move = self.get_pieces("x",x_axis_rotations.index(move)-1)

        elif move in y_axis_rotations:
            axis_of_rotation = "y"
            pieces_to_move = self.get_pieces("y",y_axis_rotations.index(move)-1)

        elif move in z_axis_rotations:
            axis_of_rotation = "z"
            pieces_to_move = self.get_pieces("z",z_axis_rotations.index(move)-1)
    
        for piece in pieces_to_move:
            self.rotate_piece(piece,axis_of_rotation,direction)
            
                

    def rotate_piece(self, piece, axis, direction=1):
        pos = piece.position
        constant_axis = self.axes[axis]
        #axis_affects has the correct axes and order for cross section
        up_axis = self.axes[self.axis_affects[axis][0]]
        along_axis = self.axes[self.axis_affects[axis][1]]
        clrs = piece.colours

        #cross section of axis of rotation
        matrix = np.array([[0,0,0],
                           [0,0,0],
                           [0,0,0]])
        
        matrix_row = 1 - pos[up_axis]
        matrix_column = pos[along_axis] + 1

        matrix[matrix_row,matrix_column] = 1

        #rotate matrix
        if (direction == 1 and pos[constant_axis]>=0)or(direction == -1 and pos[constant_axis]<0):
            matrix = np.rot90(matrix)
        elif (direction == -1 and pos[constant_axis]>=0)or(direction == 1 and pos[constant_axis]<0):
            matrix = np.rot90(matrix,3)

        result = np.where(matrix==1)

        new_position = list(zip(result[0],result[1]))
        
        piece.position[up_axis] = 1 - new_position[0][0]
        piece.position[along_axis] = new_position[0][1] - 1

        if not(piece.type == "center" and pos[constant_axis] != 0):
            piece.colours[up_axis],piece.colours[along_axis] = piece.colours[along_axis], piece.colours[up_axis]

                
        
    def get_piece(self,coordinates):
        for piece in self.pieces:
            if piece.position == coordinates:
                return piece
        return None

    def get_pieces(self, axis, value):
        pieces_selected = []
        for piece in self.pieces:
            if piece.position[self.axes[axis]] == value:
                pieces_selected.append(piece)

        return pieces_selected

    def as_list(self):
        #empty list for cube
        cube = ["?"] * 54

        convert_3d_to_2d = [
            [[0,1,0],[None,4,None]],
            [[-1,0,0],[13,None,None]],
            [[0,0,1],[None, None, 22]],
            [[1,0,0],[31,None,None]],
            [[0,0,-1],[None,None,40]],
            [[0,-1,0],[None,49,None]],

            [[-1,1,0],[10,3,None]],
            [[0,1,1],[None,7,19]],
            [[1,1,0],[28,5,None]],
            [[0,1,-1],[None,1,37]],
            [[-1,-1,0],[16,48,None]],
            [[0,-1,1],[None,46,25]],
            [[1,-1,0],[34,50,None]],
            [[0,-1,-1],[None,52,43]],
            [[-1,0,1],[14,None,21]],
            [[-1,0,-1],[12,None,41]],
            [[1,0,1],[30,None,23]],
            [[1,0,-1],[32,None,39]],

            [[-1,1,1],[11,6,18]],
            [[-1,1,-1],[9,0,38]],
            [[1,1,-1],[29,2,36]],
            [[1,1,1],[27,8,20]],
            [[-1,-1,1],[17,45,24]],
            [[-1,-1,-1],[15,51,44]],
            [[1,-1,1],[33,47,26]],
            [[1,-1,-1],[35,53,42]]
            ]
        
        for point in convert_3d_to_2d:
            piece = self.get_piece(point[0])            
            for index in range(len(point[1])):
                if point[1][index] != None:
                    cube[point[1][index]] = piece.colours[index]

        lowercase_cube = []

        for i in cube:
            lowercase_cube.append(i.lower())

        return lowercase_cube




#COLOURS
BLACK = (0,0,0)
GREY = (107,107,107)
LIGHT_GREY = (140,140,140)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
ORANGE = (255,165,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

colours_dic = {
    "w":WHITE,
    "g":GREEN,
    "r":RED,
    "o":ORANGE,
    "b":BLUE,
    "y":YELLOW
    }

colours_name = {
    "w":"White",
    "g":"Green",
    "r":"Red",
    "o":"Orange",
    "b":"Blue",
    "y":"Yellow"
    }


#Initialise PyGame
pygame.init()

#Blank Screen
size = (640,480)
screen = pygame.display.set_mode(size)

#Title
pygame.display.set_caption("Cube Solver")

#Exit flag set to false
done = False

#Manages how quick screen refreshes
clock = pygame.time.Clock()

class UI():
    def text(content, size, x, y, colour=BLACK):
        font = pygame.font.Font("freesansbold.ttf", size)
        text_surface = font.render(content,True,colour)
        text_rect = font.render(content,True,colour).get_rect()
        text_rect.center = (x,y)
        screen.blit(text_surface, text_rect)
        
    def button(msg, x, y, width, height, inactive, active, func=None, *params):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x+width > mouse[0] > x and  y+height > mouse[1] > y:
            pygame.draw.rect(screen, active, (x,y,width,height))
            if click[0] == 1 and func != None:
                if list(params) != []:
                    func(params)
                else:
                    func()
        else:
            pygame.draw.rect(screen, inactive, (x,y,width,height))

        UI.text(msg, 20, x+(width//2), y+(height//2))


    def rubix_face(x, y, width, gap, colours):
        grid_rows = [y - gap - 1.5*width ,y - width//2, y + width//2 + gap]
        grid_columns = [x - gap - 1.5*width ,x - width//2, x + width//2 + gap]

        count = 0
        for j in grid_rows:
            for i in grid_columns:
                UI.button("",i,j,width,width,colours_dic[colours[count]],colours_dic[colours[count]])
                count+=1

    def rubix_net(x,y, width, gap, colours):
        colour_list = [colours[0:9],colours[9:18],colours[18:27],colours[27:36],colours[36:45],colours[45:54]]

        one_face = 3*width + 2*gap
        face_gap = 2*gap
        spacing = one_face + face_gap
        UI.rubix_face(x,y-spacing,width,gap,colour_list[0])
        
        UI.rubix_face(x-spacing,y,width,gap,colour_list[1])
        UI.rubix_face(x,y,width,gap,colour_list[2])
        UI.rubix_face(x+spacing,y,width,gap,colour_list[3])
        UI.rubix_face(x+2*spacing,y,width,gap,colour_list[4])

        UI.rubix_face(x,y+spacing,width,gap,colour_list[5])
        
        
class ButtonFunctions():
    def solve():
        game_state.state = "solve"
        game_state.faces_scanned = 0
        game_state.cube = ""
        game_state.solution = ""

        ###TESTING SKIP
        game_state.cube = "gybbyyrryrrwbbybrwgggrrwggoobrggoyooygyyoobbwoobwwwrww"
        game_state.state = "solve_solution_screen"
        game_state.solution = solution_generator.run(game_state.cube)
        game_state.move_counter = 0
        game_state.space_being_pressed = True
        game_state.solving_cube = Virtual_Cube()
        print(game_state.solution)
        print(list(reversed(game_state.solution)))
        '''for i in reversed(game_state.solution):
            i = str(i)
            if len(i) > 1:
                if i[1] == "'":
                    game_state.solving_cube.move(i[0])
                elif i[1] == "2":
                    game_state.solving_cube.move(i[0])
                    game_state.solving_cube.move(i[0])       
                else:
                    game_state.solving_cube.move(i,-1)

        print(game_state.solving_cube.as_list())''' 
        ###TESTING SKIP END

    def confirm_adjustments():
        game_state.cube += game_state.face
        if game_state.faces_scanned < 6:
            game_state.state = "solve"
        else:
            game_state.state ="solve_solution_screen"
            game_state.move_counter = 0
            game_state.solution = solution_generator.run(game_state.cube)
            game_state.space_being_pressed = True
            game_state.solving_cube = Virtual_Cube()
            for i in reversed(game_state.solution):
                i = str(i)
                if len(i) > 1:
                    if i[1] == "'":
                        game_state.solving_cube.move(i[0],-1)
                    elif i[1] == "2":
                        game_state.solving_cube.move(i[0])
                        game_state.solving_cube.move(i[0])       
                else:
                    game_state.solving_cube.move(i)
                

    def change_colour(params):
        position = params[0]
        game_state.face = list(game_state.face)
        game_state.face[position] = game_state.equipped_colour
        game_state.face = "".join(game_state.face)

    def equip_colour(params):
        colour = params[0]
        game_state.equipped_colour = colour

    def timer():
        game_state.state = "timer"
        game_state.timer_started = False
        game_state.time_total = 0.0
        game_state.time_total_rounded = 0.0
        game_state.space_being_pressed = False
        game_state.just_stopped = False
        ButtonFunctions.generate_scramble()

    def virtual():
        game_state.shift_pressed = False
        game_state.virtual_cube = Virtual_Cube()
        
        game_state.state = "virtual"

    def learn():
        game_state.state = "learn"

    def help():
        game_state.state = "help"

    def generate_scramble():
        scramble = ""
        moves = ["L","M","R","U","F","D"]
        direction = ["","'","2"]
        previous_dir = ""
        second_previous_dir = ""
        scramble_length = 0

        while scramble_length < 16:
            next_move = random.choice(moves)
            if next_move != previous_dir and next_move != second_previous_dir:
                second_previous_dir = previous_dir
                previous_dir = next_move
                next_move = next_move + random.choices(
                    direction,
                    weights=[0.5,0.25,0.25],
                    k=1)[0]
                scramble = scramble + next_move + " "
                scramble_length += 1

        game_state.scramble = scramble

class GameState():
    def __init__(self):
        self.state = "menu"

        self.faces_to_scan = {
            "facing_camera": ["yellow","blue","red","green","orange","white"],
            "facing_up": ["orange","yellow","yellow","yellow","yellow","red"]
            }

        self.equipped_colour = "w"

    def state_manager(self):
        if self.state == "menu":
            self.menu_screen()
            
        elif self.state == "solve":
            self.solve_screen()
        elif self.state == "solve_correction_screen":
            self.solve_correction_screen()
        elif self.state == "solve_solution_screen":
            self.solve_solution_screen()
            
        elif self.state == "timer":
            self.timer_screen()
        elif self.state == "virtual":
            self.virtual_screen()
        elif self.state == "learn":
            self.learn_screen()
        elif self.state == "help":
            self.help_screen()

    def menu_screen(self):
        UI.button("Solve",220,150,200,50,GREY,LIGHT_GREY, ButtonFunctions.solve)
        UI.button("Timer",220,210,200,50,GREY,LIGHT_GREY, ButtonFunctions.timer)
        UI.button("Virtual Cube",220,270,200,50,GREY,LIGHT_GREY, ButtonFunctions.virtual)
        UI.button("Learn",220,330,200,50,GREY,LIGHT_GREY, ButtonFunctions.learn)
        UI.button("Help",220,390,200,50,GREY,LIGHT_GREY, ButtonFunctions.help)
        UI.text("CUBE SOLVER", 50, 320, 80,WHITE)

    def return_to_menu(self):
        self.state = "menu"

    def solve_screen(self):
        UI.text("SOLVER", 50, 320, 30,WHITE)
        UI.text("Please Follow The Instructions On The Other Window.", 23, 320, 240,WHITE)
        pygame.display.flip()
        

        self.face = scan_face.run(self.faces_to_scan["facing_camera"][self.faces_scanned],self.faces_to_scan["facing_up"][self.faces_scanned])
        self.faces_scanned += 1

        self.state = "solve_correction_screen" 

    def solve_correction_screen(self):
        UI.text("ADJUSTMENTS", 50, 320, 30,WHITE)
        UI.text("Please Make Any Adjustments Required Here.", 25, 320, 70,WHITE)
        UI.text("Make Sure All Parts Are Filled With The Correct Colour.", 20, 320, 100,WHITE)
        grid_width = 40
        grid_center = [160,240]
        grid_gap = 10

        grid_rows = [grid_center[1] - grid_gap - 1.5*grid_width ,grid_center[1] - grid_width//2, grid_center[1] + grid_width//2 + grid_gap]
        grid_columns = [grid_center[0] - grid_gap - 1.5*grid_width ,grid_center[0] - grid_width//2, grid_center[0] + grid_width//2 + grid_gap]

        count = 0
        for y in grid_rows:
            for x in grid_columns:
                if self.face[count] != "?":
                    UI.button("",x,y,40,40,colours_dic[self.face[count]],colours_dic[self.face[count]], ButtonFunctions.change_colour, count)
                else:
                    UI.button("?",x,y,40,40,GREY,GREY, ButtonFunctions.change_colour, count)
                count += 1

        UI.button("",410,220,40,40,WHITE,WHITE, ButtonFunctions.equip_colour, "w")
        UI.button("",460,220,40,40,GREEN,GREEN, ButtonFunctions.equip_colour, "g")
        UI.button("",510,220,40,40,BLUE,BLUE, ButtonFunctions.equip_colour, "b")
        UI.button("",410,270,40,40,RED,RED, ButtonFunctions.equip_colour, "r")
        UI.button("",460,270,40,40,ORANGE,ORANGE, ButtonFunctions.equip_colour, "o")
        UI.button("",510,270,40,40,YELLOW,YELLOW, ButtonFunctions.equip_colour, "y")
        
        UI.text("Colour Picker:", 25, 480, 190,WHITE)
        equipped_colour_text = "Equipped Colour: " + colours_name[self.equipped_colour]
        UI.text(equipped_colour_text, 20, 480, 340,WHITE)
        if "?" not in self.face:
            UI.button("Confirm",280,430,80,40,GREY,LIGHT_GREY, ButtonFunctions.confirm_adjustments)
        

    def solve_solution_screen(self):
        UI.button("Back To Menu",10,10,150,30,GREY,LIGHT_GREY, self.return_to_menu)
        UI.text("SOLVER", 50, 320, 30,WHITE)
        UI.text("Hold the cube with the red face facing you and the yellow face facing up.", 15, 320, 70,WHITE)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.space_being_pressed == False:
                self.space_being_pressed = True
                if self.move_counter + 1 < len(self.solution):
                    self.move_counter += 1
        else:
            self.space_being_pressed = False

        UI.rubix_net(140,270,20,6,self.solving_cube.as_list())
        #UI.rubix_net(140,270,20,6,self.cube)
            
        UI.text("Previous", 15, 380, 195,WHITE)
        UI.text("Moves:", 15, 380, 210,WHITE)
        if self.move_counter > 1:
            prev_move_text = str(self.solution[self.move_counter-2]) +"  "+ str(self.solution[self.move_counter-1])
        elif self.move_counter == 1:
            prev_move_text = str(self.solution[self.move_counter-1])
        else:
            prev_move_text = ""
        UI.text(prev_move_text, 25, 380, 250,WHITE)
        
        UI.text("Move:", 25, 480, 200,WHITE)
        UI.text(str(self.solution[self.move_counter]), 40, 480, 250,WHITE)
        
        UI.text("Upcoming", 15, 580, 195,WHITE)
        UI.text("Moves:", 15, 580, 210,WHITE)
        difference = (len(self.solution) - 1) - (self.move_counter + 2)
        if difference >= 0:
            upcoming_move_text = str(self.solution[self.move_counter+1]) +"  "+ str(self.solution[self.move_counter+2])
        elif difference == -1:
            upcoming_move_text = str(self.solution[self.move_counter+1])
        else:
            upcoming_move_text = ""

        UI.text(upcoming_move_text, 25, 580, 250,WHITE)

        moves_remaining_text = "Moves Remaining: " + str(len(self.solution) - 1 - self.move_counter)
        UI.text(moves_remaining_text, 15, 480, 290,WHITE)

        UI.text("Press SPACE for next move", 15, 480, 310,WHITE)
            
        #print(self.cube)
        #print(self.solution)
        
        
    def timer_screen(self):
        UI.button("Back To Menu",10,10,150,30,GREY,LIGHT_GREY, self.return_to_menu)
        UI.text("TIMER", 50, 320, 30,WHITE)

        
        UI.text(self.scramble, 25, 320, 400,WHITE)
        UI.button("Generate New Scramble",195,430,250,40,GREY,LIGHT_GREY, ButtonFunctions.generate_scramble)
        
        
        keys = pygame.key.get_pressed()

        if self.timer_started:
            self.time2 = time.time()
            self.time_total = self.time2 - self.time1
            self.time_total_rounded = round(self.time_total, 1)

        keys = pygame.key.get_pressed()
            
        if keys[pygame.K_SPACE]:
            if self.space_being_pressed == False:
                self.space_being_pressed = True

            if self.timer_started == True:
                self.timer_started = False
                self.just_stopped = True
                self.time_total_rounded = '{:.2f}'.format(round(self.time_total, 2))

        else:
            if self.space_being_pressed == True:
                self.space_being_pressed = False
                if self.timer_started == False:
                    if self.just_stopped == False:
                        self.timer_started = True
                        self.time1 = time.time()
                    else:
                        self.just_stopped = False

        UI.text(str(self.time_total_rounded), 80, 320, 240,WHITE)
            
    def virtual_screen(self):
        UI.button("Back To Menu",10,10,150,30,GREY,LIGHT_GREY, self.return_to_menu)
        UI.text("VIRTUAL", 50, 320, 30,WHITE)

        UI.rubix_net(255,270,30,10,self.virtual_cube.as_list())

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            self.shift_pressed = True
        else:
            if self.shift_pressed == True:
                self.shift_pressed = False
                
        existing_moves = ["L","M","R","D","U","B","F"]
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                letter = pygame.key.name(event.key).upper()
                if letter in existing_moves:
                    if self.shift_pressed == True:
                        self.virtual_cube.move(letter,-1)
                    else:
                        self.virtual_cube.move(letter)
                
        
    def learn_screen(self):
        UI.button("Back To Menu",10,10,150,30,GREY,LIGHT_GREY, self.return_to_menu)
        UI.text("LEARN", 50, 320, 30,WHITE)

    def help_screen(self):
        UI.button("Back To Menu",10,10,150,30,GREY,LIGHT_GREY, self.return_to_menu)
        UI.text("HELP", 50, 320, 30,WHITE)
        
        


game_state = GameState()

#Game Loop
while not done:
    
    #User input and controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    #Blank black screen
    screen.fill(BLACK)

    #Logic
    game_state.state_manager()
    
    #Flip display
    pygame.display.flip()
    
     #Clock ticks
    clock.tick(60)


pygame.quit()

