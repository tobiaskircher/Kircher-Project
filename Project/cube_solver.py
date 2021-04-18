import pygame
import scan_face
import time
import random
import solution_generator

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

class ButtonFunctions():
    def solve():
        game_state.state = "solve"
        game_state.faces_scanned = 0

    def confirm_adjustments():
        game_state.state = "solve"

    def change_colour(params):
        position = params[0]
        game_state.face = list(game_state.face)
        game_state.face[position] = game_state.equipped_colour
        "".join(game_state.face)

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

    def learn():
        game_state.state = "learn"

    def help():
        game_state.state = "help"

    def generate_scramble():
        scramble = ""
        moves = ["L","M","R","U","D","F","B"]
        direction = ["","'","2"]
        previous_dir = ""
        second_previous_dir = ""
        scramble_length = 0

        while scramble_length < 16:
            next_move = random.choice(moves)
            if next_move != previous_dir and next_move != second_previous_dir:
                second_previous_dir = previous_dir
                previous_dir = next_move
                next_move = next_move + random.choice(direction)
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

        self.cube = ""
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
        elif self.state == "learn":
            self.learn_screen()
        elif self.state == "help":
            self.help_screen()

    def menu_screen(self):
        UI.button("Solve",220,150,200,50,GREY,LIGHT_GREY, ButtonFunctions.solve)
        UI.button("Timer",220,210,200,50,GREY,LIGHT_GREY, ButtonFunctions.timer)
        UI.button("Learn",220,270,200,50,GREY,LIGHT_GREY, ButtonFunctions.learn)
        UI.button("Help",220,330,200,50,GREY,LIGHT_GREY, ButtonFunctions.help)
        UI.text("CUBE SOLVER", 50, 320, 80,WHITE)

    def return_to_menu(self):
        self.state = "menu"

    def solve_screen(self):
        UI.text("SOLVE", 50, 320, 30,WHITE)
        UI.text("Please Follow The Instructions On The Other Window.", 23, 320, 240,WHITE)
        pygame.display.flip()
        

        self.face = scan_face.run(self.faces_to_scan["facing_camera"][self.faces_scanned],self.faces_to_scan["facing_up"][self.faces_scanned])
        self.faces_scanned += 1

        if self.faces_scanned < 7:
            self.state = "solve_correction_screen"
        else:
            self.state = "solve_solution_screen"
            
        '''
        print(face[0:3])
        print(face[3:6])
        print(face[6:9])'''

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
        pass
        
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
                self.time_total_rounded = round(self.time_total, 2)

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

