import pygame

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

def test_function():
    print("Test Function Called.")

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

    text(msg, 20, x+(width//2), y+(height//2))


#Game Loop
while not done:
    
    #User input and controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    #Blank black screen
    screen.fill(BLACK)

    #Logic
    button("Solve",220,150,200,50,GREY,LIGHT_GREY, test_function)
    button("Time",220,210,200,50,GREY,LIGHT_GREY, test_function)
    button("Learn",220,270,200,50,GREY,LIGHT_GREY, test_function)
    button("Help",220,330,200,50,GREY,LIGHT_GREY, test_function)
    text("CUBE SOLVER", 50, 320, 80,WHITE)

    #Flip display
    pygame.display.flip()
    
     #Clock ticks
    clock.tick(60)


pygame.quit()

