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
marioPos = [0, 496, 0, 0, True, "Right", 0, False, 0, False, False]  # X, Y, VX, VY, onGround, direction, jumpFrames, inGround, state, isCrouch, onPlatform
    # onGround: Boolrean to see fi mario is on a solid ground
    # jumpFrames: Variable to keep track of frames user has held space for
    # inGround: Boolean to see if mario has fallen through the floor
    # state: 0 for small mario, 1 for big mario
    # onPlatform: Boolean to see if mario's last position was on a platform
marioFrame = [0, 0] # List to keep track of mario's sprites
marioAccelerate = 0.2
backPos = 0  # Position of the background
levelNum = 0  # Using 0 as level 1 since indexes start at 0
isAnimating = False  # Boolean to see if we need to pause the screen and animate mario
RECTFINDER = [0,0] #DELETE THIS LATER

# Declaring Rects

smallMario = Rect(marioPos[0], marioPos[1], 32, 64)
    
# Loading Pictures

backgroundPics = [image.load("assets/backgrounds/level_"+str(i)+".png").convert() for i in range(1,2)]

marioSpriteNames = ["smallmariojump" , "bigmariojump" , "bigmariocrouch" , "smallmariodead" , "bigmariochange"]

marioSprites = [[image.load("assets/sprites/mario/smallmario"+str(i)+".png").convert_alpha() for i in range (1,5)],
             [image.load("assets/sprites/mario/bigmario"+str(i)+".png").convert_alpha() for i in range (1,5)],
                [image.load("assets/sprites/mario/"+str(i)+".png").convert_alpha() for i in marioSpriteNames]]

brickSprites=[[image.load("assets/sprites/bricks/question"+str(1)+".png").convert_alpha() for i in range (1,4)],
              [image.load("assets/sprites/bricks/brick.png").convert_alpha(),
               image.load("assets/sprites/bricks/blockidle.png").convert_alpha()]]



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
            brickRect = Rect (brick[0], brick[1], brick[2], brick[3])
            draw.rect(screen,GREEN,brickRect)
    screen.blit(marioShow, (mario[0], mario[1]))
    display.flip()


def moveSprites(mario, marioPic, frame):
    VX, STATE, ISCROUCH = 2, 8, 9
    if mario[4]:
        frame[0] = 0 + mario[STATE]
        if frame[1] < 3.8:
            frame[1] += mario[VX]**2/100 + 0.2
        else:
            frame[1] = 1
        if frame[1] > 3.9:
            frame[1] = 3.9
        if mario[VX] == 0:
            frame[1] = 0
    else:
        frame[0],frame[1] = 2, 0+ mario[STATE]
    if mario [ISCROUCH]:
        frame[0],frame[1] = 2, 2 



def checkMovement(mario, acclerate, rectLists, pressSpace):
    """Function to move mario and the background (all rects too as a result)"""
    keys=key.get_pressed()
    X, Y, VX, VY, ONGROUND, DIR, JUMPFRAMES, INGROUND, STATE, ISCROUCH, ONPLATFORM = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    global isFalling
    moving = False
    # Walking logic
    if keys[K_a] and keys[K_d]:
        mario[VX] = 0
    elif keys[K_a] and not mario[ISCROUCH]: # Checking if mario is hitting left side of window
        if mario[DIR] != "Left":
            mario[VX] = 0  # Stop acceleration if changing direction
        walkMario(mario, rectLists, "Left")
        moving = True
        mario[DIR] = "Left"
    elif keys[K_d] and not mario[ISCROUCH]:
        if mario[DIR] != "Right":
            mario[VX] = 0 # Stop acceleration if changing direction
        walkMario(mario, rectLists, "Right")
        moving = True
        mario[DIR] = "Right"
    if keys[K_s] and mario[STATE]==1:
        mario[ISCROUCH]=True
    if mario[STATE]==0 and mario[ISCROUCH]:
        mario[ISCROUCH]=False
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
        floor=452
        marioOffset = 88
    if mario[ISCROUCH]:
        gravity = 0.9

    if mario[ONPLATFORM] and mario[VY] <= gravity*2 and pressSpace:
        isFalling = False
        mario[ONPLATFORM] = False

    if keys[K_SPACE] and not mario[ISCROUCH] and not mario[ONPLATFORM]:
        if mario[ONGROUND] and pressSpace: # checking if jumping is true
            mario[VY] -= 9.5 # jumping power
            mario[ONGROUND] = False
            mario[JUMPFRAMES] = 0
        elif mario[JUMPFRAMES] < 41 and not isFalling and not mario[ONPLATFORM]: # Simulating higher jump with less gravity
            gravity = 0.2
            mario[JUMPFRAMES] += 1

    mario[Y] += mario[VY]  # Add the y movement value

    if not mario[INGROUND] and mario[Y]>=floor and screen.get_at((int(mario[X]+4),int(mario[Y]+marioOffset)))==SKYBLUE and \
       screen.get_at((int(mario[X]+38),int(mario[Y]+marioOffset)))==SKYBLUE:
        # Using colour collision to fall through holes
        mario[INGROUND] = True
        mario[ONGROUND] = False
    elif mario[Y] >= floor and not mario[INGROUND]: # Checking floor collision
        mario[Y] = floor # stay on the ground
        mario[VY] = 0 # stop falling
        mario[ONGROUND] = True
        mario[ONPLATFORM] = False
        isFalling = False

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
            moveRects(rectLists, mario[VX])
    if mario[X] < 0:
        mario[X] = 0

def moveRects(rectLists, VX):
    global backPos
    for subList in range(len(rectLists)):
        for rect in range(len(rectLists[subList])):
            rectLists[subList][rect][0] -= VX

def checkCollide(mario, rectLists):
    global isFalling
    X, Y, VX, VY, ONGROUND, DIR, JUMPFRAMES, INGROUND, STATE, ISCROUCH, ONPLATFORM = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    height = 42
    if mario[STATE] == 1:
        height = 84
    for list in rectLists:
        for brick in list:
            brickRect = Rect(brick[0], brick[1], brick[2], brick[3])
            marioRect = Rect(mario[X] + 2, mario[Y], 38 - 2, height) # Mario's hit box (and making it a little smaller)
            if brickRect.colliderect(marioRect):
                if int(mario[Y]) + height - int(mario[VY]) <= brickRect.y:
                    mario[ONGROUND] = True
                    mario[ONPLATFORM] = True
                    isFalling = True
                    mario[VY] = 0
                    mario[Y] = brickRect.y - height
                elif mario[Y] - mario[VY] >= brickRect.y + brickRect.height:
                    mario[Y] -= mario[VY]
                    mario[VY] = 1
                    mario[Y] = brickRect.y + brickRect.height
                    mario[JUMPFRAMES] = 41
                elif mario[X] >= brickRect[X]: # and mario[DIR] == "Left":
                    mario[X] = brickRect.x + brickRect.width - 2
                    mario[VX] = 0
                elif mario[X] <= brickRect[X]: # and mario[DIR] == "Right":
                    mario[X] = brickRect.x - 38
                    mario[VX] = 0


def cycleList(rectLists):
    global backPos


# Declaring loading functions

def loadFile(targetFile):
    outputList = []
    file = open(targetFile, "r")
    fileLines = file.readlines()
    for line in fileLines:
        line = line.strip("\n")
        line = line.split(",")
        listLength = len(line)
        outputList.append([int(line[index]) for index in range(listLength)])
    return outputList

# Declaring main functions

def game():
    running = True
    while running:
        global isFalling, RECTFINDER, marioPos
        mx, my = mouse.get_pos()
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
                if evnt.key == K_0:
                    marioPos = [0, 496, 3, 0, True, "Right", 0, False, 0, False, False]
            if evnt.type == KEYUP:
                if evnt.key == K_SPACE:
                    isFalling = True
                if evnt.key== K_s:
                    marioPos[9]=False
            if evnt.type == MOUSEBUTTONDOWN:
                RECTFINDER = [mx,my]
        if key.get_pressed()[27]: running = False
        rectList = [brickList, interactBricks,questionBricks]
        checkMovement(marioPos, marioAccelerate, rectList, initialSpace)
        moveSprites(marioPos, marioSprites, marioFrame)
        checkCollide(marioPos, rectList)
        drawScene(backgroundPics[levelNum], backPos, marioPos, marioSprites, marioFrame, rectList)
        #print(RECTFINDER[0] - backPos, RECTFINDER[1], mx - RECTFINDER[0], my - RECTFINDER[1] )
        fpsCounter.tick(60)
    return "menu"


def menu():
    return 'exit'


def loading():
    running = True
    global brickList, interactBricks, questionBricks, marioPos, backPos
    marioPos = [0, 496, 0, 0, True, "Right", 0, False, 0, False, False]
    backPos = 0
    brickList = loadFile(str("data/level_" + str(levelNum+1) + "/bricks.txt"))
    interactBricks = loadFile(str("data/level_" + str(levelNum+1) + "/interactBricks.txt"))
    questionBricks = loadFile(str("data/level_" + str(levelNum+1) + "/questionBricks.txt"))
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
