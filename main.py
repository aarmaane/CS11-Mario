from pygame import *
from random import *
import os
# Starting up pygame and necessary components
os.environ['SDL_VIDEO_CENTERED'] = '1'
init()
size = width, height = 800, 600
screen = display.set_mode(size)
display.set_caption("Super Mario Bros!")
display.set_icon(transform.scale(image.load("assets/sprites/mario/smallMarioJump.png"),(32,32)))

# Declaring colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKYBLUE = (107, 140, 255)

# Declaring all fonts
marioFont = font.Font("assets/fonts/marioFont.ttf", 18)

# Declaring Variables
page = "menu"
fpsCounter = time.Clock()
marioPos = [40, 496, 0, 0, "Right", 0]  # X, Y, VX, VY, direction, state
    # onGround: Boolrean to see fi mario is on a solid ground
    # jumpFrames: Variable to keep track of frames user has held space for
    # inGround: Boolean to see if mario has fallen through the floor
    # state: 0 for small mario, 1 for big mario
    # onPlatform: Boolean to see if mario's last position was on a platform
marioStats = [True, 0, False, False, False, False] # onGround, jumpFrames, inGround, isCrouch, onPlatform, isFalling
marioFrame = [0, 0] # List to keep track of mario's sprites
marioAccelerate = 0.2
backPos = 0  # Position of the background
levelNum = 0  # Using 0 as level 1 since indexes start at 0
isAnimating = False  # Boolean to see if we need to pause the screen and animate mario
RECTFINDER = [0,0] #DELETE THIS LATER
    
# Loading Pictures
titleLogo = transform.scale(image.load("assets/sprites/title/logo.png"), (480,220))
titleSelect = transform.scale(image.load("assets/sprites/title/select.png"), (24,24))

backgroundPics = [image.load("assets/backgrounds/level_"+str(i)+".png").convert() for i in range(1,2)]

marioSpriteNames = ["smallmariojump" , "bigmariojump" , "bigmariocrouch" , "smallmariodead" , "bigmariochange"]

marioSprites = [[image.load("assets/sprites/mario/smallmario"+str(i)+".png").convert_alpha() for i in range (1,5)],
             [image.load("assets/sprites/mario/bigmario"+str(i)+".png").convert_alpha() for i in range (1,5)],
                [image.load("assets/sprites/mario/"+str(i)+".png").convert_alpha() for i in marioSpriteNames]]

brickSprites=[[image.load("assets/sprites/bricks/question"+str(1)+".png").convert_alpha() for i in range (1,4)],
              [image.load("assets/sprites/bricks/brick.gif").convert_alpha(),
               image.load("assets/sprites/bricks/blockidle.png").convert_alpha()]]

# Resizing Pictures
backgroundPics = [transform.scale(pic,(9086,600)) for pic in backgroundPics]

for subList in range(len(marioSprites)):
    for pic in range(len(marioSprites[subList])):
        if marioSprites[subList][pic].get_height() == 16:
            marioSprites[subList][pic] = transform.scale(marioSprites[subList][pic], (42, 42))
        else:
            marioSprites[subList][pic] = transform.scale(marioSprites[subList][pic], (42, 84))

for subList in range(len(brickSprites)):
    for pic in range(len(brickSprites[subList])):
        brickSprites[subList][pic] = transform.scale(brickSprites[subList][pic], (42,42))

# Creating text
playText = marioFont.render("play", False, (255,255,255))
instructText = marioFont.render("instructions", False, (255,255,255))
creditText = marioFont.render("credits", False, (255,255,255))
quitText = marioFont.render("quit", False, (255,255,255))


# Declaring game functions
def drawScene(background, backX, mario, marioPic, marioFrame, rectList, brickPic):
    """Function to draw the background, mario, enemies, and all objects"""
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    ONGROUND, JUMPFRAMES, INGROUND, ISCROUCH, ONPLATFORM, ISFALLING = 0, 1, 2, 3, 4, 5
    screen.fill(BLACK)
    screen.blit(background, (backX, 0))
    marioShow = marioPic[marioFrame[0]][int(marioFrame[1])]
    if mario[DIR] == "Left":
        marioShow = transform.flip(marioShow, True, False)
    for list in rectList:
        for brick in list:
            brickRect = Rect (brick[0], brick[1], brick[2], brick[3])
            if list == interactBricks:
                screen.blit(brickPic[1][0],brickRect)
            elif list == questionBricks:
                draw.rect(screen, BLUE, brickRect)
            else:
                draw.rect(screen,GREEN,brickRect)
    screen.blit(marioShow, (mario[0], mario[1]))
    display.flip()


def moveSprites(mario, marioInfo, marioPic, frame):
    """ Function to cycle through Mario's sprites """
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    ONGROUND, JUMPFRAMES, INGROUND, ISCROUCH, ONPLATFORM, ISFALLING = 0, 1, 2, 3, 4, 5
    if marioInfo[ONGROUND]:
        print(mario[STATE])
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
        frame[0],frame[1] = 2, 0 + mario[STATE]
    if marioInfo[ISCROUCH]:
        frame[0],frame[1] = 2, 2 



def checkMovement(mario, marioInfo, acclerate, rectLists, pressSpace):
    """Function to accept inputs and apply the appropriate physics """
    keys = key.get_pressed()
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    ONGROUND, JUMPFRAMES, INGROUND, ISCROUCH, ONPLATFORM, ISFALLING = 0, 1, 2, 3, 4, 5
    moving = False
    # Walking logic
    if keys[K_a] and keys[K_d]:
        mario[VX] = 0
    elif keys[K_a] and not marioInfo[ISCROUCH]: # Checking if mario is hitting left side of window
        if mario[DIR] != "Left":
            mario[VX] = 0  # Stop acceleration if changing direction
        walkMario(mario, rectLists, "Left")
        moving = True
        mario[DIR] = "Left"
    elif keys[K_d] and not marioInfo[ISCROUCH]:
        if mario[DIR] != "Right":
            mario[VX] = 0 # Stop acceleration if changing direction
        walkMario(mario, rectLists, "Right")
        moving = True
        mario[DIR] = "Right"
    if keys[K_s] and mario[STATE]==1:
        marioInfo[ISCROUCH]=True
    if mario[STATE]==0 and marioInfo[ISCROUCH]:
        marioInfo[ISCROUCH]=False
    if moving: # Accelerate if there is input
        if marioInfo[ONGROUND]:
            mario[VX] += acclerate
        else:
            mario[VX] += acclerate/4 # Slow down movement when midair
    elif mario[VX] != 0: # Move and decelerate if there is no input
        if mario[DIR] == "Right":
            walkMario(mario, rectLists, "Right")
        if mario[DIR] == "Left":
            walkMario(mario, rectLists, "Left")
        if marioInfo[ONGROUND]: # Don't decelerate mid air
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
    if marioInfo[ISCROUCH]:
        gravity = 0.9

    if marioInfo[ONPLATFORM] and mario[VY] <= gravity*2 and pressSpace:
        marioInfo[ISFALLING] = False
        marioInfo[ONPLATFORM] = False

    if keys[K_SPACE] and not marioInfo[ISCROUCH] and not marioInfo[ONPLATFORM]:
        if marioInfo[ONGROUND] and pressSpace: # checking if jumping is true
            mario[VY] -= 9.5 # jumping power
            marioInfo[ONGROUND] = False
            marioInfo[JUMPFRAMES] = 0
            if mario[STATE] == 0:
                playSound("effects/smallJump.ogg", "effect")
            else:
                playSound("effects/bigJump.ogg", "effect")
        elif marioInfo[JUMPFRAMES] < 41 and not marioInfo[ISFALLING] and not marioInfo[ONPLATFORM]: # Simulating higher jump with less gravity
            gravity = 0.2
            marioInfo[JUMPFRAMES] += 1

    mario[Y] += mario[VY]  # Add the y movement value

    if not marioInfo[INGROUND] and mario[Y]>=floor and screen.get_at((int(mario[X]+4),int(mario[Y]+marioOffset)))==SKYBLUE and \
       screen.get_at((int(mario[X]+38),int(mario[Y]+marioOffset)))==SKYBLUE:
        # Using colour collision to fall through holes
        marioInfo[INGROUND] = True
        marioInfo[ONGROUND] = False
    elif mario[Y] >= floor and not marioInfo[INGROUND]: # Checking floor collision
        mario[Y] = floor # stay on the ground
        mario[VY] = 0 # stop falling
        marioInfo[ONGROUND] = True
        marioInfo[ONPLATFORM] = False
        marioInfo[ISFALLING] = False

    marioPos[VY] += gravity # apply gravity


def walkMario(mario, rectLists, direction):
    """ Function to move the player """
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
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
    """ Function to move rectangles """
    global backPos
    for subList in range(len(rectLists)):
        for rect in range(len(rectLists[subList])):
            rectLists[subList][rect][0] -= VX

def checkCollide(mario, marioInfo, rectLists):
    """ Function to check mario's collision with Rects"""
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    ONGROUND, JUMPFRAMES, INGROUND, ISCROUCH, ONPLATFORM, ISFALLING = 0, 1, 2, 3, 4, 5
    height = 42
    if mario[STATE] == 1:
        height = 84
    for list in rectLists:
        for brick in list:
            brickRect = Rect(brick[0], brick[1], brick[2], brick[3])
            marioRect = Rect(mario[X] + 2, mario[Y], 38 - 2, height) # Mario's hit box (and making it a little smaller)
            if brickRect.colliderect(marioRect):
                if int(mario[Y]) + height - int(mario[VY]) <= brickRect.y:
                    marioInfo[ONGROUND] = True
                    marioInfo[ONPLATFORM] = True
                    marioInfo[ISFALLING] = True
                    mario[VY] = 0
                    mario[Y] = brickRect.y - height
                elif mario[Y] - mario[VY] >= brickRect.y + brickRect.height:
                    mario[Y] -= mario[VY]
                    mario[VY] = 1
                    mario[Y] = brickRect.y + brickRect.height
                    marioInfo[JUMPFRAMES] = 41
                    playSound("effects/bump.ogg", "effect")
                elif mario[X] >= brickRect[X]: # and mario[DIR] == "Left":
                    mario[X] = brickRect.x + brickRect.width - 2
                    mario[VX] = 0
                elif mario[X] <= brickRect[X]: # and mario[DIR] == "Right":
                    mario[X] = brickRect.x - 38
                    mario[VX] = 0

def playSound(soundFile, soundChannel):
    """ Function to load in sounds and play them on a channel """
    channelList = [["music", 0], ["effect", 1]]
    for subList in channelList:
        if subList[0] == soundChannel:
            channelNumber = subList[1]
    soundObject = mixer.Sound("assets/music/" + soundFile)
    mixer.Channel(channelNumber).stop()
    mixer.Channel(channelNumber).play(soundObject)

def globalSound(command, volume = None):
    """ Function to apply commands to all mixer channels """
    for id in range(mixer.get_num_channels()):
        if command == "stop":
            mixer.Channel(id).stop()
        elif command == "pause":
            mixer.Channel(id).pause()
        elif command == "unpause":
            mixer.Channel(id).unpause()
        elif command == "volume":
            mixer.Channel(id).set_volume(volume)

def cycleList(rectLists):
    """ Function to keep track of objects on screen and ignore others"""
    global backPos


# Declaring loading functions

def loadFile(targetFile):
    """ Function to load files and make lists out of them"""
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
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    ONGROUND, JUMPFRAMES, INGROUND, ISCROUCH, ONPLATFORM, ISFALLING = 0, 1, 2, 3, 4, 5
    global marioStats, RECTFINDER, marioPos
    playSound("songs/mainSong.ogg", "music")
    startTime = time.get_ticks()
    while running:
        mx, my = mouse.get_pos()
        initialSpace = False
        for evnt in event.get():
            if evnt.type == QUIT:
                running = False
            if evnt.type == KEYDOWN:
                if evnt.key == K_SPACE:
                    initialSpace = True
                if evnt.key == K_p:
                    if marioPos[STATE] == 0:
                        marioPos[STATE] = 1
                    else:
                        marioPos[STATE] = 0
                if evnt.key == K_0:
                    marioPos = [0, 496, 0, 0, "Right", 0]
                    marioStats = [True, 0, False, False, False, False]
            if evnt.type == KEYUP:
                if evnt.key == K_SPACE:
                    marioStats[ISFALLING] = True
                if evnt.key== K_s:
                    marioStats[ISCROUCH]=False
            if evnt.type == MOUSEBUTTONDOWN:
                RECTFINDER = [mx,my]
        if key.get_pressed()[27]: running = False
        rectList = [brickList, interactBricks,questionBricks]
        checkMovement(marioPos, marioStats, marioAccelerate, rectList, initialSpace)
        moveSprites(marioPos, marioStats, marioSprites, marioFrame)
        checkCollide(marioPos, marioStats, rectList)
        drawScene(backgroundPics[levelNum], backPos, marioPos, marioSprites, marioFrame, rectList, brickSprites)
        print(RECTFINDER[0] - backPos, RECTFINDER[1], mx - RECTFINDER[0], my - RECTFINDER[1] )
        fpsCounter.tick(60)
    return "menu"


def menu():
    running = True
    globalSound("stop") # Stop any music that's playing
    selected = 0 # Variable for current selected option
    textPoints = [[360, 350], [290, 390], [333, 430], [360, 470]]
    textList = [playText, instructText, creditText, quitText]
    returnList = ["loading", "instructions", "credits", "exit"]
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                running = False
            if evnt.type == KEYDOWN:
                if evnt.key == K_UP or evnt.key == K_w:
                    selected -= 1
                elif evnt.key == K_DOWN or evnt.key == K_s:
                    selected += 1
                elif evnt.key == K_RETURN:
                    return returnList[selected]
        if selected < 0:
            selected = 3
        elif selected > 3:
            selected = 0
        screen.blit(backgroundPics[0],(0,0))
        screen.blit(marioSprites[0][0], (40, 496))
        screen.blit(titleLogo,(160,80))
        for index in range(len(textList)):
            screen.blit(textList[index], (textPoints[index][0], textPoints[index][1]))
        screen.blit(titleSelect, (textPoints[selected][0] - 30, textPoints[selected][1] - 4 ))
        display.flip()
        fpsCounter.tick(60)
    return "exit"


def loading():
    running = True
    global brickList, interactBricks, questionBricks, marioPos, backPos, marioStats
    marioPos = [40, 496, 0, 0, "Right", 0]
    marioStats = [True, 0, False, False, False, False]
    backPos = 0
    brickList = loadFile(str("data/level_" + str(levelNum+1) + "/bricks.txt"))
    interactBricks = loadFile(str("data/level_" + str(levelNum+1) + "/interactBricks.txt"))
    questionBricks = loadFile(str("data/level_" + str(levelNum+1) + "/questionBricks.txt"))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[K_RETURN]: running = False
        tempText = marioFont.render("LOADING...", False, (255,255,255))
        screen.blit(tempText,(0,0))
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
