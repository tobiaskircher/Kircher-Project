import pygame
import scan_face

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
        '''face = scan_face.run()
        print(face[0:3])
        print(face[3:6])
        print(face[6:9])'''

    def timer():
        game_state.state = "timer"

    def learn():
        game_state.state = "learn"

    def help():
        game_state.state = "help"

def get_face():
    face = scan_face.run()
    return face

class GameState():
    def __init__(self):
        self.state = "menu"

        self.faces_to_scan = {
            "facing_camera": ["Green","Red","Blue","Orange","White","Yellow"],
            "facing_up": ["White","White","White","White","Green","Blue"]
            }

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
        get_face()
        
    def timer_screen(self):
        UI.button("Back To Menu",10,10,150,30,GREY,LIGHT_GREY, self.return_to_menu)
        UI.text("TIMER", 50, 320, 30,WHITE)

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

