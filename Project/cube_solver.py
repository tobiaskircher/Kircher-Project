#CUBE SOLVER

#Import required libraries
import pygame, time, random, webbrowser
import numpy as np

#Import the face scanning file
import scan_face, solution_generator


#VIRTUAL CUBE CLASS

#Class which defines pieces
class Piece():
    def __init__(self, position, colours):
        #[0,0,0] being centre piece (does not exist, in middle of cube)
        self.position = position
        #[clr facing x dir, clr facing y dir, clr facing z dir]
        self.colours = colours

        #Count number of colours on the piece
        colour_count = 0
        for colour in colours:
            if colour != None:
                colour_count+=1

        #Determine the type of piece depending on how many colours it has
        if colour_count == 1:
            self.type = "center"
        elif colour_count == 2:
            self.type = "edge"
        elif colour_count == 3:
            self.type = "corner"

    #Change how piece is represented when printed
    #(USED FOR TESTING)
    def __str__(self):
        line1 = "Position: " + str(self.position)
        line2 = "Colours: " + str(self.colours)
        return line1 + "\n" + line2

#Class which defines an entire 3x3 Rubik's cube
class Virtual_Cube():
    def __init__(self):
        #initiate cube pieces
        #orientation: yellow facing up, red facing towards you

        #Set up all the pieces
        
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

        #List containing all the pieces on the cube
        self.pieces = [
            self.y, self.b, self.r, self.g, self.o, self.w,
            self.yb, self.yr, self.yg, self.yo,
            self.wb, self.wr, self.wg, self.wo,
            self.br, self.bo, self.gr, self.go,
            self.ybr, self.ybo, self.ygr, self.ygo,
            self.wbr, self.wbo, self.wgr, self.wgo
        ]

        #Variables for axes
        self.axes= {"x":0,
               "y":1,
               "z":2
               }
        
        #Note: Each rotation on an axis affects another axis of the pieces value
        #For example r affects all pieces with x=1, but it changes their y and z values
        self.axis_affects = {"x":["y","z"],
                             "y":["z","x"],
                             "z":["x","y"]
                             }

    #Function to make a move on the Rubik's cube
    def move(self, move, direction=None):
        
        #Decide on direction of move
        if direction == None: direction = 1
        else: direction = -1

        #Put moves in groups depending on what axis they rotate on
        x_axis_rotations = ["L", "M", "R"]
        y_axis_rotations = ["D", None, "U"]
        z_axis_rotations = ["B", None, "F"]

        #Get pieces to rotate on x axis
        if move in x_axis_rotations:
            axis_of_rotation = "x"
            pieces_to_move = self.get_pieces("x",x_axis_rotations.index(move)-1)

        #Get pieces to rotate on y axis
        elif move in y_axis_rotations:
            axis_of_rotation = "y"
            pieces_to_move = self.get_pieces("y",y_axis_rotations.index(move)-1)

        #Get pieces to rotate on z axis
        elif move in z_axis_rotations:
            axis_of_rotation = "z"
            pieces_to_move = self.get_pieces("z",z_axis_rotations.index(move)-1)

        #Rotate each piece involved in the move
        for piece in pieces_to_move:
            self.rotate_piece(piece,axis_of_rotation,direction)
            if direction == 2:
                self.rotate_piece(piece,axis_of_rotation,direction)
            

    #Rotate single piece
    def rotate_piece(self, piece, axis, direction=1):
        #Get position
        pos = piece.position
        
        #Get axis it is rotating on
        constant_axis = self.axes[axis]
        
        #axis_affects has the correct axes for cross section
        up_axis = self.axes[self.axis_affects[axis][0]]
        along_axis = self.axes[self.axis_affects[axis][1]]

        #Get colours
        clrs = piece.colours

        #cross section of axis of rotation represented in matrix
        matrix = np.array([[0,0,0],
                           [0,0,0],
                           [0,0,0]])

        #Get position of piece in the matrix
        matrix_row = 1 - pos[up_axis]
        matrix_column = pos[along_axis] + 1

        #Represent the piece being moved in the matrix
        matrix[matrix_row,matrix_column] = 1

        #Rotate matrix in the correct direction
        if (direction == 1 and pos[constant_axis]>=0)or(direction == -1 and pos[constant_axis]<0):
            matrix = np.rot90(matrix)
        elif (direction == -1 and pos[constant_axis]>=0)or(direction == 1 and pos[constant_axis]<0):
            matrix = np.rot90(matrix,3)

        #Find new position of piece
        result = np.where(matrix==1)

        #Put new position in a list
        new_position = list(zip(result[0],result[1]))

        #Assign new position to piece
        piece.position[up_axis] = 1 - new_position[0][0]
        piece.position[along_axis] = new_position[0][1] - 1

        #Update direction the colours on the piece are facing
        if not(piece.type == "center" and pos[constant_axis] != 0):
            piece.colours[up_axis],piece.colours[along_axis] = piece.colours[along_axis], piece.colours[up_axis]

                
    #Function to get the piece in a specific position
    def get_piece(self,coordinates):
        #Iterate through pieces and return the correct piece
        for piece in self.pieces:
            if piece.position == coordinates:
                return piece
        #Return none if no piece is in that position
        return None

    #Function to get several pieces on an axis
    #e.g. get pieces with x value of 1
    def get_pieces(self, axis, value):
        #List for pieces
        pieces_selected = []
        #Add each piece with the correct value on chosen axis to the list
        for piece in self.pieces:
            if piece.position[self.axes[axis]] == value:
                pieces_selected.append(piece)

        #return pieces
        return pieces_selected

    def as_list(self):
        #Empty list for cube
        cube = ["?"] * 54

        #List mapping 3D coordinates to position in list
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

        #Convert the 3D cube to the 2D list
        for point in convert_3d_to_2d:
            piece = self.get_piece(point[0])            
            for index in range(len(point[1])):
                if point[1][index] != None:
                    cube[point[1][index]] = piece.colours[index]

        #Convert cube to lowercase
        lowercase_cube = []
        for i in cube:
            lowercase_cube.append(i.lower())

        #Return cube
        return lowercase_cube




#Define colours
BLACK = (0,0,0)
GREY = (107,107,107)
LIGHT_GREY = (140,140,140)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
ORANGE = (255,165,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

#Assign colours to letter code
colours_dic = {
    "w":WHITE,
    "g":GREEN,
    "r":RED,
    "o":ORANGE,
    "b":BLUE,
    "y":YELLOW
    }

#Assign full colour name to their letter representation
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

#Class to handle UI
class UI():

    #Function which draws text to screen
    def text(content, size, x, y, colour=BLACK):
        font = pygame.font.Font("freesansbold.ttf", size)
        text_surface = font.render(content,True,colour)
        text_rect = font.render(content,True,colour).get_rect()
        text_rect.center = (x,y)
        screen.blit(text_surface, text_rect)

    #Function which draws button to screen and handles its functionality
    def button(msg, x, y, width, height, inactive, active, func=None, *params):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        #Draw active button
        if x+width > mouse[0] > x and  y+height > mouse[1] > y:
            pygame.draw.rect(screen, active, (x,y,width,height))
            
            #If clicked, call function associated with button
            if click[0] == 1 and func != None and game_state.can_click == True:
                game_state.can_click = False
                if list(params) != []:
                    func(params)
                else:
                    func()
                    
        #Draw inactive button
        else:
            pygame.draw.rect(screen, inactive, (x,y,width,height))

        #Draw text on top of button
        UI.text(msg, 20, x+(width//2), y+(height//2))


    #Function which draws Rubik's face onto screen
    def rubix_face(x, y, width, gap, colours):
        
        #Decide on postions for rows and coloumns
        grid_rows = [y - gap - 1.5*width ,y - width//2, y + width//2 + gap]
        grid_columns = [x - gap - 1.5*width ,x - width//2, x + width//2 + gap]

        #Draw face
        count = 0
        for j in grid_rows:
            for i in grid_columns:
                UI.button("",i,j,width,width,colours_dic[colours[count]],colours_dic[colours[count]])
                count+=1

    #Function to draw entire Rubik's net onto screen
    def rubix_net(x,y, width, gap, colours):
        #Split colours into list
        colour_list = [colours[0:9],colours[9:18],colours[18:27],colours[27:36],colours[36:45],colours[45:54]]

        #Set up size of face and spacing
        one_face = 3*width + 2*gap
        face_gap = 2*gap
        spacing = one_face + face_gap

        #Draw all 6 faces
        UI.rubix_face(x,y-spacing,width,gap,colour_list[0])
        
        UI.rubix_face(x-spacing,y,width,gap,colour_list[1])
        UI.rubix_face(x,y,width,gap,colour_list[2])
        UI.rubix_face(x+spacing,y,width,gap,colour_list[3])
        UI.rubix_face(x+2*spacing,y,width,gap,colour_list[4])

        UI.rubix_face(x,y+spacing,width,gap,colour_list[5])
        

class ButtonFunctions():
    #Function when solve button is pressed
    def solve():
        #Initialise required variables
        game_state.state = "solve"
        game_state.faces_scanned = 0
        game_state.cube = ""
        game_state.solution = ""

    #Function pressed to confirm manual adjustments to face
    def confirm_adjustments():
        #Increment amount of faces inputted
        game_state.faces_scanned += 1
        game_state.cube += game_state.face

        #If not all faces scanned, scan next face
        if game_state.faces_scanned < 6:
            game_state.state = "solve"

        #Else proceed to solution screen
        else:
            game_state.state = "solve_solution_screen"

            #Attempt to create solution to Rubik's cube
            try:
                game_state.solution = solution_generator.run(game_state.cube)

                #Insert empty move
                game_state.solution.insert(0," ")
                
                #Initialise variables
                game_state.move_counter = 0
                game_state.space_being_pressed = True
                game_state.solving_cube = Virtual_Cube()

                #Reverse solution and perform it on the cube
                #(As the inital cube is solved, we need to make it like the user's one)
                for i in list(reversed(game_state.solution)):
                    i = str(i)
                    if len(i) > 1:
                        if i[1] == "'":
                            game_state.solving_cube.move(i[0])
                        elif i[1] == "2":
                            game_state.solving_cube.move(i[0])
                            game_state.solving_cube.move(i[0])       
                    elif i != " ":
                        game_state.solving_cube.move(i,-1)

            #Go to error screen if cube can't be solved
            except:
                game_state.state = "unsolvable_screen"
                

    #Function to change colour on face
    def change_colour(params):
        position = params[0]
        #Convert face to list
        game_state.face = list(game_state.face)
        #Update colour
        game_state.face[position] = game_state.equipped_colour
        #Convert back to string
        game_state.face = "".join(game_state.face)

    #Function to equip a new colour
    def equip_colour(params):
        colour = params[0]
        #Update attribute with chosen colour
        game_state.equipped_colour = colour

    #Function before timer screen is drawn
    def timer():
        #Initialise required variables
        game_state.state = "timer"
        game_state.timer_started = False
        game_state.time_total = 0.0
        game_state.time_total_rounded = 0.0
        game_state.space_being_pressed = False
        game_state.just_stopped = False

        #Make a scramble to display
        ButtonFunctions.generate_scramble()

    #Function called before virtual mode is opened
    def virtual():
        #Initialise attributes
        game_state.shift_pressed = False
        game_state.virtual_cube = Virtual_Cube()
        
        game_state.state = "virtual"

    #Function to reset virtual cube
    def reset_virtual_cube():
        game_state.virtual_cube = Virtual_Cube()

    #Function to scramble virtual cube
    def scramble_virtual_cube():
        
        #Create scramble
        ButtonFunctions.generate_scramble()

        #Perform moves on virtual Rubik's cube
        for i in game_state.scramble.split():
            if len(i) > 1:
                if i[1] == "'":
                    game_state.virtual_cube.move(i[0],-1)
                elif i[1] == "2":
                    game_state.virtual_cube.move(i[0])
                    game_state.virtual_cube.move(i[0])       
            else:
                game_state.virtual_cube.move(i)      

    #Function called when "Learn" is pressed
    def learn():
        #Update screen that user is currently on
        game_state.state = "learn"

    #Function called when "Help" is pressed
    def help():
        #Update screen that user is currently on
        game_state.state = "help"

    #Function to generate a scramble
    def generate_scramble():

        #Make empty string
        scramble = ""

        #Define moves and directions
        moves = ["L","M","R","U","F","D"]
        direction = ["","'","2"]

        #Store previous moves to avoid repetition
        previous_dir = ""
        second_previous_dir = ""

        #Length counter
        scramble_length = 0

        #Create scramble with 16 moves
        while scramble_length < 16:
            #Pick random move
            next_move = random.choice(moves)
            #If move is different to last two moves
            if next_move != previous_dir and next_move != second_previous_dir:
                #Update previous moves
                second_previous_dir = previous_dir
                previous_dir = next_move
                #Add direction to next move
                next_move = next_move + random.choices(
                    direction,
                    weights=[0.5,0.25,0.25],
                    k=1)[0]
                #Add move to scramble
                scramble = scramble + next_move + " "
                #Increment scramble length
                scramble_length += 1

        #Assign scramble to the relevant attribute
        game_state.scramble = scramble

    #Function to make move
    def text_move(movement):
        #If not a standard move
        if len(movement) > 1:
            #Make move depending on direction
            if movement[1] == "'":
                game_state.solving_cube.move(movement[0],-1)
            elif movement[1] == "2":
                game_state.solving_cube.move(movement[0])
                game_state.solving_cube.move(movement[0])
        #Else perform standard move
        else:
            game_state.solving_cube.move(movement)
            
    #Function to open link in users web browser
    def open_link(link):
        webbrowser.open(link[0])        

#Class which handles what is shown on the screen (UI)         
class GameState():

    #Initialise object
    def __init__(self):
        #Start on menu screen
        self.state = "menu"

        #Faces to scan including orientation
        self.faces_to_scan = {
            "facing_camera": ["yellow","blue","red","green","orange","white"],
            "facing_up": ["orange","yellow","yellow","yellow","yellow","red"]
            }

        #Default equipped colour set to white
        self.equipped_colour = "w"

        #Allow user to click
        self.can_click = True

        #Save Help screen image into variable
        self.help_screen_img = pygame.transform.scale(pygame.image.load("help_screen.jpg").convert(), (640,430))

    #Manage what screen the user is currently on
    def state_manager(self):

        #Manage if the user can click or not
        click = pygame.mouse.get_pressed()
        if click[0] == 0:
            self.can_click = True

        #Draw the correct screen
        if self.state == "menu":
            self.menu_screen()
        elif self.state == "solve":
            self.solve_screen()
        elif self.state == "solve_correction_screen":
            self.solve_correction_screen()
        elif self.state == "solve_solution_screen":
            self.solve_solution_screen()
        elif self.state == "unsolvable_screen":
            self.unsolvable_screen() 
        elif self.state == "timer":
            self.timer_screen()
        elif self.state == "virtual":
            self.virtual_screen()
        elif self.state == "learn":
            self.learn_screen()
        elif self.state == "help":
            self.help_screen()


    #Menu screen
    def menu_screen(self):
        #Draw buttons
        UI.button("Solve",220,150,200,50,GREY,LIGHT_GREY, ButtonFunctions.solve)
        UI.button("Timer",220,210,200,50,GREY,LIGHT_GREY, ButtonFunctions.timer)
        UI.button("Virtual Cube",220,270,200,50,GREY,LIGHT_GREY, ButtonFunctions.virtual)
        UI.button("Learn",220,330,200,50,GREY,LIGHT_GREY, ButtonFunctions.learn)
        UI.button("Help",220,390,200,50,GREY,LIGHT_GREY, ButtonFunctions.help)
        
        #Draw title
        UI.text("CUBE SOLVER", 50, 320, 80,WHITE)


    #Return user to menu
    def return_to_menu(self):
        self.state = "menu"


    #Solve screen (getting input)
    def solve_screen(self):
        #Draw title and intructions
        UI.text("SOLVER", 50, 320, 30,WHITE)
        UI.text("Please Follow The Instructions On The Other Window.", 23, 320, 240,WHITE)
        pygame.display.flip()
        
        #Attempt to scan face
        self.face = scan_face.run(self.faces_to_scan["facing_camera"][self.faces_scanned],self.faces_to_scan["facing_up"][self.faces_scanned])

        #If no camera is detected, return blank face
        if self.face == "nocamera":
            self.no_camera = True
            self.face = "?????????"
        else:
            self.no_camera = False

        #Move to the correction screen
        self.state = "solve_correction_screen" 


    #Manual adjustments screen
    def solve_correction_screen(self):
        #Draw title and instructions
        UI.text("ADJUSTMENTS", 50, 320, 30,WHITE)
        UI.text("Please Make Any Adjustments Required Here.", 25, 320, 70,WHITE)
        UI.text("Make Sure All Parts Are Filled With The Correct Colour.", 20, 320, 100,WHITE)

        #If there was no camera, let the user know what face to input
        if self.no_camera == True:
            print(self.faces_scanned)
            UI.text("No Camera Was Detected!", 20, 320, 130,RED)
            faces_text = "Scan with "+self.faces_to_scan["facing_camera"][self.faces_scanned]+ " face facing camera,"+ \
                         " and with "+self.faces_to_scan["facing_up"][self.faces_scanned]+ " face facing up."
            UI.text(faces_text, 15, 320, 160,RED)

        #Set up grid size and location
        grid_width = 40
        grid_center = [160,240]
        grid_gap = 10
        
        #Define location for rows and columns
        grid_rows = [grid_center[1] - grid_gap - 1.5*grid_width ,grid_center[1] - grid_width//2, grid_center[1] + grid_width//2 + grid_gap]
        grid_columns = [grid_center[0] - grid_gap - 1.5*grid_width ,grid_center[0] - grid_width//2, grid_center[0] + grid_width//2 + grid_gap]

        #Draw each square on the face with the correct colour
        count = 0
        for y in grid_rows:
            for x in grid_columns:
                if self.face[count] != "?":
                    UI.button("",x,y,40,40,colours_dic[self.face[count]],colours_dic[self.face[count]], ButtonFunctions.change_colour, count)
                else:
                    UI.button("?",x,y,40,40,GREY,GREY, ButtonFunctions.change_colour, count)
                count += 1

        #Draw buttons so user can change equipped colour
        UI.button("",410,220,40,40,WHITE,WHITE, ButtonFunctions.equip_colour, "w")
        UI.button("",460,220,40,40,GREEN,GREEN, ButtonFunctions.equip_colour, "g")
        UI.button("",510,220,40,40,BLUE,BLUE, ButtonFunctions.equip_colour, "b")
        UI.button("",410,270,40,40,RED,RED, ButtonFunctions.equip_colour, "r")
        UI.button("",460,270,40,40,ORANGE,ORANGE, ButtonFunctions.equip_colour, "o")
        UI.button("",510,270,40,40,YELLOW,YELLOW, ButtonFunctions.equip_colour, "y")

        #Draw text for the colour equipper
        UI.text("Colour Picker:", 25, 480, 190,WHITE)
        equipped_colour_text = "Equipped Colour: " + colours_name[self.equipped_colour]
        UI.text(equipped_colour_text, 20, 480, 340,WHITE)

        #Show the continue button once there are no missing colours
        if "?" not in self.face:
            UI.button("Confirm",280,430,80,40,GREY,LIGHT_GREY, ButtonFunctions.confirm_adjustments)

        
    #Solution screen
    def solve_solution_screen(self):
        #Draw back to menu button
        UI.button("Back To Menu",10,10,150,30,GREY,LIGHT_GREY, self.return_to_menu)

        #Draw title and instructions
        UI.text("SOLVER", 50, 320, 30,WHITE)
        UI.text("Hold the cube with the red face facing you and the yellow face facing up.", 15, 320, 70,WHITE)

        #Continue to next move if space was pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.space_being_pressed == False:
                self.space_being_pressed = True
                #Perform next move (if there is one) on virtual cube
                if self.move_counter + 1 < len(self.solution):
                    self.move_counter += 1
                    move_string = str(self.solution[self.move_counter])
                    ButtonFunctions.text_move(move_string)
        else:
            self.space_being_pressed = False

        #Draw virtual rubik's cube to screen
        UI.rubix_net(130,270,20,6,self.solving_cube.as_list())

        #Display previous moves
        UI.text("Previous", 15, 380, 195,WHITE)
        UI.text("Moves:", 15, 380, 210,WHITE)
        if self.move_counter > 1:
            prev_move_text = str(self.solution[self.move_counter-2]) +"  "+ str(self.solution[self.move_counter-1])
        elif self.move_counter == 1:
            prev_move_text = str(self.solution[self.move_counter-1])
        else:
            prev_move_text = ""
        UI.text(prev_move_text, 25, 380, 250,WHITE)

        #Display current move
        UI.text("Move:", 25, 480, 200,WHITE)
        UI.text(str(self.solution[self.move_counter]), 40, 480, 250,WHITE)

        #Display upcoming moves
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

        #Display how many remaining moves there are
        moves_remaining_text = "Moves Remaining: " + str(len(self.solution) - 1 - self.move_counter)
        UI.text(moves_remaining_text, 15, 480, 290,WHITE)

        #Put text with more instructions on the screen
        UI.text("Press SPACE for next move", 15, 480, 310,WHITE)
            

    #Unsolvable cube error screen
    def unsolvable_screen(self):
        #Draw back to menu button
        UI.button("Back To Menu",10,10,150,30,GREY,LIGHT_GREY, self.return_to_menu)

        #Draw title and error message
        UI.text("SOLVER", 50, 320, 30,WHITE)
        UI.text("The Rubik's cube you inputted is unsolvable.", 23, 320, 240,RED)
        UI.text("This may be to misinput or a twisted corner/edge.", 23, 320, 260,RED)
        UI.text("Please go to back to the menu and try again.", 23, 320, 280,RED)
        

    #Timer screen
    def timer_screen(self):
        #Create back to menu button and title
        UI.button("Back To Menu",10,10,150,30,GREY,LIGHT_GREY, self.return_to_menu)
        UI.text("TIMER", 50, 320, 30,WHITE)

        #Show scramble and button to create a new one        
        UI.text(self.scramble, 25, 320, 400,WHITE)
        UI.button("Generate New Scramble",195,430,250,40,GREY,LIGHT_GREY, ButtonFunctions.generate_scramble)

        #Update time if timer is running
        if self.timer_started:
            self.time2 = time.time()
            self.time_total = self.time2 - self.time1
            self.time_total_rounded = round(self.time_total, 1)

        #Get key pressed
        keys = pygame.key.get_pressed()

        #If space is pressed
        if keys[pygame.K_SPACE]:
            #Show space is currently being pressed
            if self.space_being_pressed == False:
                self.space_being_pressed = True

            #If timer was running, stop it
            if self.timer_started == True:
                self.timer_started = False
                self.just_stopped = True
                self.time_total_rounded = '{:.2f}'.format(round(self.time_total, 2))

        else:
            #Update that spacebar is not being pressed
            if self.space_being_pressed == True:
                self.space_being_pressed = False

                #Start timer if spacebar was released
                if self.timer_started == False:
                    if self.just_stopped == False:
                        self.timer_started = True
                        self.time1 = time.time()
                    else:
                        #Allow the timer to be started again once previous keystroke was finished
                        self.just_stopped = False

        #Draw time on screen
        UI.text(str(self.time_total_rounded), 80, 320, 240,WHITE)


    #Virtual Rubik's cube screen
    def virtual_screen(self):
        #Draw title and buttons
        UI.button("Back To Menu",10,10,150,30,GREY,LIGHT_GREY, self.return_to_menu)
        UI.text("VIRTUAL", 50, 320, 30,WHITE)
        UI.button("Scramble",420,430,100,40,GREY,LIGHT_GREY, ButtonFunctions.scramble_virtual_cube)
        UI.button("Solve",540,430,80,40,GREY,LIGHT_GREY, ButtonFunctions.reset_virtual_cube)

        #Draw Rubik's cube net
        UI.rubix_net(255,270,30,10,self.virtual_cube.as_list())

        #Get pressed key
        keys = pygame.key.get_pressed()
        
        #Check if left shift was pressed
        if keys[pygame.K_LSHIFT]:
            self.shift_pressed = True
        else:
            if self.shift_pressed == True:
                self.shift_pressed = False

        #Define moves that the user can make
        existing_moves = ["L","M","R","D","U","B","F"]

        #Execute move on the Virtual Rubik's cube
        for event in pygame.event.get():

            #If button is pressed down
            if event.type == pygame.KEYDOWN:
                #Convert to uppercase
                letter = pygame.key.name(event.key).upper()
                #And execute move it is valid
                if letter in existing_moves:
                    #Perform move in correct direction, depending if LShift is being pressed
                    if self.shift_pressed == True:
                        self.virtual_cube.move(letter,-1)
                    else:
                        self.virtual_cube.move(letter)
                        
            #Close software if close button is clicked
            if event.type == pygame.QUIT:
                done = True
                
    #Learn screen
    def learn_screen(self):
        #Draw back to menu button and title
        UI.button("Back To Menu",10,10,150,30,GREY,LIGHT_GREY, self.return_to_menu)
        UI.text("LEARN", 50, 320, 30,WHITE)
        
        #Paragraph 1
        UI.text("The Rubik's cube was invented in 1974 by a professor of", 20, 320, 60,WHITE)
        UI.text("architecture called Ernő Rubik. Since then it has become", 20, 320, 80,WHITE)
        UI.text("a world-renowned puzzle and many sophisticated methods for", 20, 320, 100,WHITE)
        UI.text("solving it have been created.", 20, 320, 120,WHITE)

        #Paragraph 2
        UI.text("The easiest method to learn is called the \"Beginner's Method\".", 20, 320, 150,WHITE)
        UI.text("Then there are more complex methods which focus more on time", 20, 320, 170,WHITE)
        UI.text("taken to solve the cube, for example CFOP.", 20, 320, 190,WHITE)

        #Paragraph 3
        UI.text("Moves are mainly written using Rubik's cube notation, which is", 20, 320, 220,WHITE)
        UI.text("also used in the software. Learn more about it by following the", 20, 320, 240,WHITE)
        UI.text("relevant link below.", 20, 320, 260,WHITE)

        #Buttons which open links in web browser
        UI.text("Links:", 20, 320, 300,WHITE)
        UI.button("More about the history",170,310,300,30,GREY,LIGHT_GREY, ButtonFunctions.open_link,"https://www.rubiks.com/en-uk/about")
        UI.button("Learn Rubik's cube notation",170,350,300,30,GREY,LIGHT_GREY, ButtonFunctions.open_link,"https://ruwix.com/the-rubiks-cube/notation/")
        UI.button("Learn the Beginner's Method",170,390,300,30,GREY,LIGHT_GREY, ButtonFunctions.open_link,"https://ruwix.com/the-rubiks-cube/how-to-solve-the-rubiks-cube-beginners-method/")
        UI.button("Learn CFOP",170,430,300,30,GREY,LIGHT_GREY, ButtonFunctions.open_link,"https://jperm.net/3x3/cfop")
        

    #Help screen
    def help_screen(self):
        #Draw back to menu button and title
        UI.button("Back To Menu",10,10,150,30,GREY,LIGHT_GREY, self.return_to_menu)
        UI.text("HELP", 50, 320, 30,WHITE)

        #Put image of help screen on the screen
        screen.blit(self.help_screen_img,(0,50))
        
        

#Create instance of UI
game_state = GameState()

#GAME LOOP
while not done:
    
    #End software if the close ("X") button in pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    #Blank black screen
    screen.fill(BLACK)

    #Logic - let class handle what screen to draw
    game_state.state_manager()
    
    #Flip display
    pygame.display.flip()
    
    #Clock ticks
    clock.tick(60)

#Once program is closed, terminate pygame and end software
pygame.quit()

#END

