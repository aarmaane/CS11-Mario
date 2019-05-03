from pygame import *
from random import *
from os import *
# Starting up pygame and necessary components
environ['SDL_VIDEO_CENTERED'] = '1'
init()
size = width, height = 800, 600
screen = display.set_mode(size)
display.set_caption("Super Mario Bros!")

# Declaring colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKYBLUE = (247, 214, 181)

# Declaring Variables

page = "game"
fpsCounter = time.Clock()
marioPos = [0, 496, 3, 0, True, "Right"]  # X, Y, VX, VY, ONGROUND, Direction
marioAccelerate = 1
backPos = [0]  # Position of the background (as list because mutability)
marioState = 0  # 0 is small, 1 is big mario
levelNum = 0  # Using 0 as level 1 since indexes start at 0
marioSpriteNames = ["smallmariojump" , "bigmariojump" , "bigmariocrouch" , "smallmariodead" , "bigmariochange"]
isAnimating = False  # Boolean to see if we need to pause the screen and animate mario

# Declaring Rects

smallMario = Rect(marioPos[0], marioPos[1], 32, 64)
    
# Loading Pictures

backgroundPics = [image.load("assets/backgrounds/level_"+str(i)+".png").convert() for i in range(1,2)]

marioSprites = [[image.load("assets/sprites/mario/smallmario"+str(i)+".png").convert_alpha() for i in range (1,5)],
             [image.load("assets/sprites/mario/bigmario"+str(i)+".png").convert_alpha() for i in range (1,5)],
                [image.load("assets/sprites/mario/"+str(i)+".png").convert_alpha() for i in marioSpriteNames]]

# Resizing Pictures
backgroundPics = [transform.scale(pic,(9086,600)) for pic in backgroundPics]

for i in range(4):
    marioSprites[0][i] = transform.scale(marioSprites[0][i], (42, 42))
    marioSprites[1][i] = transform.scale(marioSprites[1][i], (42, 96))

# Declaring game functions

def drawScene(background, backX, mario, marioPic):
    """Function to draw the background, mario, enemies, and all objects"""
    screen.blit(background, (backX[0], 0))
    screen.blit(marioPic[0][0], (mario[0], mario[1]))


def checkMovement(mario, acclerate, backX, rectLists):
    """Function to move mario and the background (all rects too as a result)"""
    keys=key.get_pressed()
    moving = False
    if keys[K_a]: # Checking if mario is hitting left side of window
        walkMario(mario, backX, rectLists, "Left")
        moving = True
        mario[5] = "Left"
    if keys[K_d]:
        walkMario(mario, backX, rectLists, "Right")
        moving = True
        mario[5] = "Right"
	if moving:
		mario[2] += acclerate
    if moving == False and mario[2] != 0:
        if mario[5] == "Right":
            walkMario(mario, backX, rectLists, "Right")
        if mario[5] == "Left":
            walkMario(mario, backX, rectLists, "Left")
        mario[2] -= acclerate
    floor=496
    if marioState==1:
        floor=442
    if keys[K_SPACE] and marioPos[4]: # checking if jumping is true
        marioPos[3]-=10 # jumping power
        marioPos[4]=False
    marioPos[1]+=marioPos[3]
    
    if marioPos[1]>=floor:
        marioPos[1]=floor # stay on the ground
        marioPos[3]=0 # stop falling
        marioPos[4]=True
        
    marioPos[3]+=0.3 # apply gravity

    # Max and min acceleration
    if mario[2] > 7:
        mario[2] = 7
    elif mario[2] < 0:
        mario[2] = 0


def walkMario(mario, backX, rectLists, direction):
    if direction == "Left" and mario[0] != 1:
        mario[0] -= mario[2]  # Subtracting the VX
    elif direction == "Right":
        if mario[0] < 368: # Checking if mario is in the middle of the screen
            mario[0] += mario[2] # Adding the VX
        else:
            mario[0] = 368
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
        checkMovement(marioPos, marioAccelerate, backPos, 0)
        drawScene(backgroundPics[levelNum], backPos, marioPos, marioSprites)
        print(marioPos)
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
