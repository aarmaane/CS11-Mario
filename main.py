from pygame import *
from random import *
import os
# Starting up pygame and necessary components
os.environ['SDL_VIDEO_CENTERED'] = '1'
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

page = "loading"
fpsCounter = time.Clock()
marioPos = [0, 496, 3, 0, True, "Right", 0, False, 0]  # X, Y, VX, VY, onGround, direction, jumpFrames, inGround, state
    # onGround: Boolrean to see fi mario is on a solid ground
    # jumpFrames: Variable to keep track of frames user has held space for
    # inGround: Boolean to see if mario has fallen through the floor
    # state: 0 for small mario, 1 for big mario
marioFrame = [0, 0]
marioAccelerate = 0.2
backPos = 0  # Position of the background
levelNum = 0  # Using 0 as level 1 since indexes start at 0
jumpFrames = 0 # Checking frames that user has been jumping for
isAnimating = False  # Boolean to see if we need to pause the screen and animate mario


# Declaring Rects

smallMario = Rect(marioPos[0], marioPos[1], 32, 64)
    
# Loading Pictures

backgroundPics = [image.load("assets/backgrounds/level_"+str(i)+".png").convert() for i in range(1,2)]

marioSpriteNames = ["smallmariojump" , "bigmariojump" , "bigmariocrouch" , "smallmariodead" , "bigmariochange"]

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
            marioSprites[subList][pic] = transform.scale(marioSprites[subList][pic], (42, 84))

# Declaring game functions

def drawScene(background, backX, mario, marioPic, marioFrame, rectList):
    """Function to draw the background, mario, enemies, and all objects"""
    screen.fill(BLACK)
    screen.blit(background, (backX, 0))
    marioShow = marioPic[marioFrame[0]][int(marioFrame[1])]
    if mario[5] == "Left":
        marioShow = transform.flip(marioShow, True, False)
    for list in rectList:
        for brick in list:
            draw.rect(screen,GREEN,brick)
    screen.blit(marioShow, (mario[0], mario[1]))
    display.flip()


def moveSprites(mario, marioPic, frame):
    VX, STATE = 2, 8
    if mario[4]:
        frame[0] = 0 + mario[STATE]
        if frame[1] < 3.8:
            frame[1] +=  mario[VX]**2/100 + 0.2
        else:
            frame[1] = 1
        if frame[1] > 3.9:
            frame[1] = 3.9
        if mario[VX] == 0:
            frame[1] = 0
    else:
        frame[0],frame[1] = 2, 0+ mario[STATE]


def checkMovement(mario, acclerate, rectLists, pressSpace):
    """Function to move mario and the background (all rects too as a result)"""
    keys=key.get_pressed()
    X, Y, VX, VY, ONGROUND, DIR, JUMPFRAMES, INGROUND, STATE = 0, 1, 2, 3, 4, 5, 6, 7, 8
    global isFalling
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
            mario[VX] += acclerate/4 # Slow down movement when midair
    elif mario[VX] != 0: # Move and decelerate if there is no input
        if mario[DIR] == "Right":
            walkMario(mario, rectLists, "Right")
        if mario[DIR] == "Left":
            walkMario(mario, rectLists, "Left")
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
    marioOffset = 42
    if mario[STATE]==1: # Change values if mario is big
        floor=450
        marioOffset = 88
    if keys[K_SPACE]:
        if mario[ONGROUND] and pressSpace: # checking if jumping is true
            mario[VY] -= 9.5 # jumping power
            mario[ONGROUND] = False
            isFalling = False
            mario[JUMPFRAMES] = 0
        elif mario[JUMPFRAMES] < 41 and not isFalling: # Simulating higher jump with less gravity
            gravity = 0.2
            mario[JUMPFRAMES] += 1
    mario[Y] += marioPos[VY]  # Add the y movement value
    if mario[Y]>=floor and not mario[INGROUND]: # Checking floor collision
        mario[Y]=floor # stay on the ground
        mario[VY]=0 # stop falling
        mario[ONGROUND]=True
    if mario[Y]==floor and screen.get_at((int(mario[X]+4),int(mario[Y]+marioOffset)))==SKYBLUE and \
       screen.get_at((int(mario[X]+38),int(mario[Y]+marioOffset)))==SKYBLUE:
        # Using colour collision to fall through holes
        mario[INGROUND] = True
        mario[ONGROUND] = False
    marioPos[VY] += gravity # apply gravity
    print(jumpFrames)


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

# Declaring loading functions

def loadFile(targetFile):
    outputList = []
    file = open(targetFile, "r")
    fileLines = file.readlines()
    for line in fileLines:
        line = line.split(",")
        outputList.append(Rect(int(line[0]),int(line[1]),int(line[2]),int(line[3])))
    return outputList

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
                if evnt.key == K_p:
                    if marioPos[8] == 0:
                        marioPos[8] = 1
                    else:
                        marioPos[8] = 0
            if evnt.type == KEYUP:
                if evnt.key == K_SPACE:
                    isFalling = True
        if key.get_pressed()[27]: running = False
        rectList = [brickList]
        checkMovement(marioPos, marioAccelerate, 0, initialSpace)
        moveSprites(marioPos, marioSprites, marioFrame)
        drawScene(backgroundPics[levelNum], backPos, marioPos, marioSprites, marioFrame, rectList)
        fpsCounter.tick(60)
    return "menu"


def menu():
    return 'exit'


def loading():
    running = True
    global brickList
    brickList = loadFile(str("data/level_" + str(levelNum+1) + "/bricks.txt"))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[K_RETURN]: running = False
        screen.blit(backgroundPics[0], (0,0))
        display.flip()
        fpsCounter.tick(60)
    return "game"


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
    if page == "loading":
        page = loading()
    if page == "game":
        page = game()
    if page == "instructions":
        page = instructions()     
    if page == "credit":
        page = credit()
quit()
