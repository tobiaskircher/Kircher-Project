#Free Mode
class Piece():
    def __init__(self, position, colours):
        #[0,0,0] being centre piece (does not exist, in middle of cube)
        self.position = position
        #[clr facing x dir, clr facing y dir, clr facing z dir]
        self.colours = colours

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
        self.r = Piece([0,0,-1],[None,None,"R"])
        self.g = Piece([1,0,0],["G",None,None])
        self.o = Piece([0,0,1],[None,None,"O"])
        self.w = Piece([0,-1,0],[None,"W",None])

        #edge pieces
        #eg. yb = yellow + blue edge piece
        self.yb = Piece([-1,1,0],["B","Y",None])
        self.yr = Piece([0,1,-1],[None,"Y","R"])
        self.yg = Piece([1,1,0],["G","Y",None])
        self.yo = Piece([0,1,1],[None,"Y","O"])
        self.wb = Piece([-1,-1,0],["B","W",None])
        self.wr = Piece([0,-1,-1],[None,"W","R"])
        self.wg = Piece([1,-1,0],["G","W",None])
        self.wo = Piece([0,-1,-1],[None,"W","O"])
        self.br = Piece([-1,0,-1],["B",None,"R"])
        self.bo = Piece([-1,0,1],["B",None,"O"])
        self.gr = Piece([1,0,-1],["G",None,"R"])
        self.go = Piece([1,0,1],["G",None,"O"])

        #corner pieces
        #eg ybr = yellow+blue+red corner piece
        self.ybr = Piece([-1,1,-1],["B","Y","R"])
        self.ybo = Piece([-1,1,1],["B","Y","O"])
        self.ygr = Piece([1,1,-1],["G","Y","O"])
        self.ygo = Piece([1,1,1],["G","Y","R"])
        self.wbr = Piece([-1,-1,-1],["B","W","R"])
        self.wbo = Piece([-1,-1,1],["B","W","O"])
        self.wgr = Piece([1,-1,-1],["G","W","R"])
        self.wgo = Piece([1,-1,1],["G","W","O"])

        self.pieces = [
            self.y, self.b, self.r, self.g, self.o, self.w,
            self.yb, self.yr, self.yg, self.yo,
            self.wb, self.wr, self.wg, self.wo,
            self.br, self.bo, self.gr, self.go,
            self.ybr, self.ybo, self.ygr, self.ygo,
            self.wbr, self.wbo, self.wgr, self.wgo
        ]

    def get_piece(self,coordinates):
        for piece in self.pieces:
            if piece.position == coordinates:
                return piece
        return None

    def __str__(self):
        return "Print cube."
                




test_piece = Piece([1,0,-1],["B","W",None])
test_cube = Cube()
#print(test_cube)
print(test_cube.get_piece([1,1,1]))
