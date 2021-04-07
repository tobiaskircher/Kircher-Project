import pygame

BLACK = (0,0,0)
WHITE = (255,255,255)

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

#Game Loop
while not done:
    
    #User input and controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    #Blank black screen
    screen.fill (BLACK)

    #Flip display
    pygame.display.flip()
    
     #Clock ticks
    clock.tick(60)


pygame.quit()

