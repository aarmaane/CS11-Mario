from pygame import *
from random import *
from os import *
# Starting up pygame and necessary components
environ['SDL_VIDEO_CENTERED'] = '1'
init()
size = width, height = 800, 600
screen = display.set_mode(size)
# Declaring colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Declaring Variables

page = "game"
fpsCounter = time.Clock()
marioPos = [0, 470, 3, 0, True] # X, Y, VX, VY, ONGROUND
backPos = [0] # Position of the background (as list because mutability)
marioSprites = []
marioState = 0 # 0 is small, 1 is big mario
levelNum = 0 # Using 0 as level 1 since indexes start at 0

# Declaring Rects

smallMario = Rect(marioPos[0], marioPos[1], 32, 64)
    
# Loading Pictures
backgroundPics = [image.load("assets/backgrounds/level_"+str(i)+".png").convert() for i in range(1,2)]
backgroundPics = [transform.smoothscale(pic,(9086,600)) for pic in backgroundPics]

# Declaring game functions

def drawScene(background, backX):
    """Function to draw the background, mario, enemies, and all objects"""
    screen.blit(background, (backX[0], 0))
    draw.rect(screen, RED, (marioPos[0], marioPos[1], 32, 64))

def moveMario(mario, backX, rectLists):
    """Function to move mario and the background (all rects too as a result)"""
    keys=key.get_pressed()
    if keys[K_a] and mario[0]!=1: # Checking if mario is hitting left side of window
        mario[0] -= mario[2] # Subtracting the VX
    if keys[K_d]:
        if mario[0] < 401: # Checking if mario is in the middle of the screen
            mario[0] += mario[2] # Adding the VX
        else:
            backX[0] -= mario[2] # Subtracting the VX from the background
    if mario[0] < 0:
        mario[0] = 0

# Declaring main functions

def game():
    running = True
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False
        screen.fill(BLACK)
        drawScene(backgroundPics[levelNum], backPos)
        moveMario(marioPos, backPos, 0)
        print(marioPos,backPos)
        display.flip()
        fpsCounter.tick(60)
    return "menu"


def menu():
    return 'exit'

def loading():
    running = True
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False
        display.flip()
        fpsCounter.tick(60)
    return "menu"

def instructions():
    running = True
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False
        display.flip()
        fpsCounter.tick(60)
    return "menu"
        
def credit():
    running = True
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False
        display.flip()
        fpsCounter.tick(60)
    return "menu"


while page != "exit":
    if page == "menu":
        page = menu()
    if page == "game":
        page = game()
    if page == "instructions":
        page = instructions()     
    if page == "credit":
        page = credit()  
    

quit()
