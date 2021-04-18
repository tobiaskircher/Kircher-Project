import pygame
import scan_face
import time
import random
import solution_generator

BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (107,107,107)
LIGHT_GREY = (140,140,140)

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
        
    def button(msg, x, y, width, height, inactive, active, func=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x+width > mouse[0] > x and  y+height > mouse[1] > y:
            pygame.draw.rect(screen, active, (x,y,width,height))
            if click[0] == 1 and func != None:
                func()
        else:
            pygame.draw.rect(screen, inactive, (x,y,width,height))

        UI.text(msg, 20, x+(width//2), y+(height//2))

class ButtonFunctions():
    def solve():
        game_state.state = "solve"
        game_state.faces_scanned = 0

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

    def state_manager(self):
        if self.state == "menu":
            self.menu_screen()
        elif self.state == "solve":
            self.solve_screen()
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
        

        face = scan_face.run(self.faces_to_scan["facing_camera"][self.faces_scanned],self.faces_to_scan["facing_up"][self.faces_scanned])
        self.faces_scanned += 1
        '''print("\n")
        print(self.faces_to_scan["facing_camera"][count])
        print(face[0:3])
        print(face[3:6])
        print(face[6:9])
        count += 1'''

    def correction_screen(self):
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

