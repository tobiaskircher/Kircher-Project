 #Virtual Cube

import numpy as np

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
        
class Cube():
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
                
        

    def __str__(self):
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

        #create net
        text = ""
        
        #yellow face
        for i in range(0,9,3):
            text += (" " * 4) + "".join(cube[i:i+3]) + "\n"
        text += "\n"
        
        #blue, red, green and orange face
        line1, line2, line3 = "","",""
        for i in range(1,5):
            line1 += "".join(cube[i*9:i*9+3])+ " "
            line2 += "".join(cube[i*9+3:i*9+6]) + " "
            line3 += "".join(cube[i*9+6:i*9+9]) + " "
        line1 += "\n"
        line2 += "\n"
        line3 += "\n"

        text += line1 + line2 + line3

        #white face
        text += "\n"
        for i in range(45,53,3):
            text += (" " * 4) + "".join(cube[i:i+3]) + "\n"
        
        return text
    

test_cube = Cube()
print(test_cube)
while True:
    move = input("Input move: ")
    if move == "end":
        break
    else:
        try:
            if len(move) > 1:
                if move[1] == "'":
                    test_cube.move(move[0],-1)
            else:
                test_cube.move(move)
            print(test_cube)
        except:
            print("Invalid input.")
