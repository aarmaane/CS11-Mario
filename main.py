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

frame=0
page = "game"
fpsCounter = time.Clock()
marioPos = [0, 496, 3, 0, True, "Right"]  # X, Y, VX, VY, ONGROUND, Direction
marioAccelerate = 0.6
backPos = [0]  # Position of the background (as list because mutability)
marioState = 0  # 0 is small, 1 is big mario
levelNum = 0  # Using 0 as level 1 since indexes start at 0
jumpFrames = [0] # Checking frames that user has been jumping for
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

for subList in marioSprites:
    for pic in subList:
        if pic.get_height() == 16:
            pic = transform.scale(pic, (42, 42))
        else:
            pic = transform.scale(pic, (42, 92))
# Declaring game functions

def drawScene(background, backX, mario, marioPic):
    """Function to draw the background, mario, enemies, and all objects"""
    screen.blit(background, (backX[0], 0))
    screen.blit(marioPic[0][0], (mario[0], mario[1]))
    screen.blit(marioSprites[marioState][frame],(mario[0],mario[1]))

def moveSprites(mario,marioSprite,marioState,frame):
    pass
    #if frame +=0.8
    

def checkMovement(mario, acclerate, backX, rectLists, jumpFrames):
    """Function to move mario and the background (all rects too as a result)"""
    keys=key.get_pressed()
    X, Y, VX, VY, ONGROUND, DIR = 0, 1, 2, 3, 4, 5
    moving = False
    ####DEBUG INPUT
    if keys[K_r]:
        backX[0] = 0
    # Walking logic
    if keys[K_a]: # Checking if mario is hitting left side of window
        if mario[DIR] != "Left":
            mario[VX] = 0 # Stop acceleration if changing direction
        walkMario(mario, backX, rectLists, "Left")
        moving = True
        mario[DIR] = "Left"
    if keys[K_d]:
        if mario[DIR] != "Right":
            mario[VX] = 0 # Stop acceleration if changing direction
        walkMario(mario, backX, rectLists, "Right")
        moving = True
        mario[DIR] = "Right"
    if moving: # Accelerate if there is input
        if mario[ONGROUND]:
            mario[VX] += acclerate
        else:
            mario [VX] += acclerate/4 # Slow down movement when midair
    elif mario[VX] != 0: # Move and decelerate if there is no input
        if mario[DIR] == "Right":
            walkMario(mario, backX, rectLists, "Right")
        if mario[DIR] == "Left":
            walkMario(mario, backX, rectLists, "Left")
        if mario[ONGROUND]: # Don't decelerate mid air
            mario[VX] -= acclerate
    # Max and min acceleration
    if mario[VX] > 5:
        mario[VX] = 5
    elif mario[VX] < 0:
        mario[VX] = 0
    # Jumping logic
    gravity = 0.6
    floor=496
    if marioState==1:
        floor=442
    if keys[K_SPACE]:
        if mario[ONGROUND]: # checking if jumping is true
            mario[VY] -= 9.5 # jumping power
            mario[ONGROUND] = False
            jumpFrames[0] = 0
        elif jumpFrames[0] < 80:
            gravity = 0.2
            jumpFrames[0] += 1
    mario[Y] += marioPos[VY]  # Add the y movement value
    if mario[Y] < 311:
        jumpFrames[0] = 80
    if mario[Y]>=floor:
        mario[Y]=floor # stay on the ground
        mario[VY]=0 # stop falling
        mario[ONGROUND]=True
    if mario[Y]==floor and mario[Y]-1.get_at()==SKYBLUE:
        mario[Y]-=1
        
    marioPos[VY] += gravity # apply gravity
    print(jumpFrames)


def walkMario(mario, backX, rectLists, direction):
    X, Y, VX, VY, ONGROUND, DIR = 0, 1, 2, 3, 4, 5
    if direction == "Left" and mario[X] != 1:
        mario[X] -= mario[VX]  # Subtracting the VX
    elif direction == "Right":
        if mario[X] < 368: # Checking if mario is in the middle of the screen
            mario[X] += mario[VX] # Adding the VX
        else:
            mario[X] = 368
            backX[0] -= mario[VX] # Subtracting the VX from the background
    if mario[X] < 0:
        mario[X] = 0





# Declaring main functions

def game():
    running = True
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False
        screen.fill(BLACK)
        checkMovement(marioPos, marioAccelerate, backPos, 0, jumpFrames)
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
