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
    
def button(text, x, y, width, height, inactive, active, func=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+width > mouse[0] > x and  y+height > mouse[1] > y:
        pygame.draw.rect(screen, active, (x,y,width,height))
        if click[0] == 1 and func != None:
            func()
    else:
        pygame.draw.rect(screen, inactive, (x,y,width,height))

    font = pygame.font.Font("freesansbold.ttf",20)
    text_surface, text_rect = font.render(text,True,BLACK), font.render(text,True,BLACK).get_rect()
    text_rect.center = (x+(width//2),y+(height//2))
    screen.blit(text_surface, text_rect)

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

    #Flip display
    pygame.display.flip()
    
     #Clock ticks
    clock.tick(60)


pygame.quit()

