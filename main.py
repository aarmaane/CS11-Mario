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
SKYBLUE = (107, 140, 255)

# Declaring Variables

page = "game"
fpsCounter = time.Clock()
marioPos = [0, 496, 3, 0, True, "Right"]  # X, Y, VX, VY, ONGROUND, Direction
marioFrame = [0,0]
marioAccelerate = 0.5
backPos = 0  # Position of the background (as list because mutability)
marioState = 0  # 0 is small, 1 is big mario
levelNum = 0  # Using 0 as level 1 since indexes start at 0
jumpFrames = 0 # Checking frames that user has been jumping for
marioSpriteNames = ["smallmariojump" , "bigmariojump" , "bigmariocrouch" , "smallmariodead" , "bigmariochange"]
isAnimating = False  # Boolean to see if we need to pause the screen and animate mario
isFalling = False # Boolean to see if the user has let go of the jump button

# Declaring Rects

smallMario = Rect(marioPos[0], marioPos[1], 32, 64)
    
# Loading Pictures

backgroundPics = [image.load("assets/backgrounds/level_"+str(i)+".png").convert() for i in range(1,2)]

marioSprites = [[image.load("assets/sprites/mario/smallmario"+str(i)+".png").convert_alpha() for i in range (1,5)],
             [image.load("assets/sprites/mario/bigmario"+str(i)+".png").convert_alpha() for i in range (1,5)],
                [image.load("assets/sprites/mario/"+str(i)+".png").convert_alpha() for i in marioSpriteNames]]

# Resizing Pictures
backgroundPics = [transform.scale(pic,(9086,600)) for pic in backgroundPics]

for subList in range(len(marioSprites)):
    for pic in range(len(marioSprites[subList])):
        if marioSprites[subList][pic].get_height() == 16:
            marioSprites[subList][pic] = transform.scale(marioSprites[subList][pic], (42, 42))
        else:
            marioSprites[subList][pic] = transform.scale(marioSprites[subList][pic], (42, 92))
# Declaring game functions

def drawScene(background, backX, mario, marioPic, marioFrame):
    """Function to draw the background, mario, enemies, and all objects"""
    screen.blit(background, (backX, 0))
    print(marioFrame)
    marioShow = marioPic[marioFrame[0]][int(marioFrame[1])]
    if mario[5] == "Left":
        marioShow = transform.flip(marioShow, True, False)

    screen.blit(marioShow, (mario[0], mario[1]))


def moveSprites(mario,marioSprite,marioState,frame):
    global marioFrame
    VX = 2
    if mario[4]:
        marioFrame[0] = 0 + marioState
        if marioFrame[1] < 3.8 and mario[VX] != 0:
            marioFrame[1] +=  mario[VX]**2/100 + 0.2
        else:
            marioFrame[1] = 0
        if marioFrame[1] > 3.9:
            marioFrame[1] = 3.9
    else:
        marioFrame = [2,0+marioState]


def checkMovement(mario, marioState, acclerate, rectLists, pressSpace):
    """Function to move mario and the background (all rects too as a result)"""
    keys=key.get_pressed()
    X, Y, VX, VY, ONGROUND, DIR = 0, 1, 2, 3, 4, 5
    global jumpFrames, isFalling
    moving = False
    # Walking logic
    if keys[K_a]: # Checking if mario is hitting left side of window
        if mario[DIR] != "Left":
            mario[VX] = 0  # Stop acceleration if changing direction
        walkMario(mario, rectLists, "Left")
        moving = True
        mario[DIR] = "Left"
    if keys[K_d]:
        if mario[DIR] != "Right":
            mario[VX] = 0 # Stop acceleration if changing direction
        walkMario(mario, rectLists, "Right")
        moving = True
        mario[DIR] = "Right"
    if moving: # Accelerate if there is input
        if mario[ONGROUND]:
            mario[VX] += acclerate
        else:
            mario [VX] += acclerate/4 # Slow down movement when midair
    elif mario[VX] != 0: # Move and decelerate if there is no input
        if mario[DIR] == "Right":
            walkMario(mario, rectLists, "Right")
        if mario[DIR] == "Left":
            walkMario(mario, rectLists, "Left")
        if mario[ONGROUND]: # Don't decelerate mid air
            mario[VX] -= acclerate
    # Max and min acceleration
    if mario[VX] > 4:
        mario[VX] = 4
    elif mario[VX] < 0:
        mario[VX] = 0
    # Jumping logic
    gravity = 0.6
    floor=496
    if marioState==1:
        floor=442
    if keys[K_SPACE]:
        if mario[ONGROUND] and pressSpace: # checking if jumping is true
            mario[VY] -= 9.5 # jumping power
            mario[ONGROUND] = False
            isFalling = False
            jumpFrames = 0
        elif jumpFrames < 80 and not isFalling:
            gravity = 0.2
            jumpFrames += 1
    mario[Y] += marioPos[VY]  # Add the y movement value
    if mario[Y] < 311:
        isFalling = True
    if mario[Y]>=floor:
        mario[Y]=floor # stay on the ground
        mario[VY]=0 # stop falling
        mario[ONGROUND]=True
    if mario[Y]==floor and screen.get_at((int(mario[X]).int(mario[Y])))==SKYBLUE:
        mario[Y]-=10
    marioPos[VY] += gravity # apply gravity


def walkMario(mario, rectLists, direction):
    X, Y, VX, VY, ONGROUND, DIR = 0, 1, 2, 3, 4, 5
    global backPos
    if direction == "Left" and mario[X] != 1:
        mario[X] -= mario[VX]  # Subtracting the VX
    elif direction == "Right":
        if mario[X] < 368: # Checking if mario is in the middle of the screen
            mario[X] += mario[VX] # Adding the VX
        else:
            mario[X] = 368
            backPos -= mario[VX] # Subtracting the VX from the background
    if mario[X] < 0:
        mario[X] = 0





# Declaring main functions

def game():
    running = True
    while running:
        global isFalling
        initialSpace = False
        for evnt in event.get():
            if evnt.type == QUIT:
                running = False
            if evnt.type == KEYDOWN:
                if evnt.key == K_SPACE:
                    initialSpace = True
            if evnt.type == KEYUP:
                if evnt.key == K_SPACE:
                    isFalling = True
        if key.get_pressed()[27]: running = False
        screen.fill(BLACK)
        checkMovement(marioPos, marioState, marioAccelerate, 0, initialSpace)
        moveSprites(marioPos, marioSprites, marioState, marioFrame)
        drawScene(backgroundPics[levelNum], backPos, marioPos, marioSprites, marioFrame)
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
