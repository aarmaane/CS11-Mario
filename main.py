from pygame import *
import copy
import os
# Starting up pygame and necessary components
os.environ['SDL_VIDEO_CENTERED'] = '1'  # Centering the screen
init()  # Starting up pygame
size = width, height = 800, 600
screen = display.set_mode(size)
display.set_caption("Super Mario Bros!")  # Setting the window title
display.set_icon(transform.scale(image.load("assets/sprites/mario/smallMarioJump.png"),(32,32)))  # Setting the screen icon

# Declaring colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKYBLUE = (107, 140, 255)

# Declaring Variables
page = "menu"  # Variable for the current game state
fpsCounter = time.Clock()  # FPS counter
marioPos = [40, 496, 0, 0, "Right", 0]  # X, Y, VX, VY, direction, state
# X, Y: Variables to keep track of mario's position on screen
# VX, VY:  Variables to keep track of mario's X and Y velocity
# direction: Variable to keep track of the direction mario is facing
# state: 0 for small mario, 1 for big mario
marioStats = [True, 0, False, False, False, False, False, 0] # onGround, jumpFrames, inGround, isCrouch, onPlatform, isFalling, isAnimating, invulFrames
# onGround: Boolean to see if mario is on a solid ground
# jumpFrames: Variable to keep track of frames user has held space for
# inGround: Boolean to see if mario has fallen through the floor
# isCrouch: Boolean to see if mario is crouching
# onPlatform: Boolean to see if mario's last position was on a platform
# isFalling: Boolean to see if mario has stopped jumping and should fall
# isAnimating: Boolean to see if we need to pause the game and change mario's state
# invulFrames: Variable to keep track of the frames where mario is invulnerable
marioScore = [0, 0, 5]  # Points, Coins, Lives
marioFrame = [0, 0, 0]  # List to keep track of mario's sprites and his changing animation
marioAccelerate = 0.2  # The rate at which mario can speed up and slow down
backPos = 0  # Position of the background
levelNum = 0  # Variable to keep track of the current level
selected = 0  # Variable for current selected option in menu


# Loading Pictures
titleLogo = transform.scale(image.load("assets/sprites/title/logo.png"), (480,220))
titleSelect = transform.scale(image.load("assets/sprites/title/select.png"), (24,24))
mutePic = transform.scale(image.load("assets/sprites/title/muted.png"), (45,45))

backgroundPics = [transform.scale(image.load("assets/backgrounds/level_1.png").convert(), (9086, 600)),
                  transform.scale(image.load("assets/backgrounds/level_2.png").convert(), (10065, 600)),
                  transform.scale(image.load("assets/backgrounds/level_3.png").convert(), (9200, 600)),
                  transform.scale(image.load("assets/backgrounds/level_4.png").convert(), (16380, 600)),
                  transform.scale(image.load("assets/backgrounds/level_5.png").convert(), (10000, 600))]

winPics = [transform.scale(image.load("assets/backgrounds/win.png").convert(), (800, 600)),
            transform.scale(image.load("assets/sprites/title/peach.png").convert(), (42, 69))]

marioSpriteNames = ["smallmariojump" , "bigmariojump" , "bigmariocrouch" , "smallmariodead" , "bigmariochange", "smallmariochange"]
marioSpriteNamesFlag = ["flagsmall1", "flagsmall2", "flagbig1", "flagbig2", "flagsmall2", "flagbig2"]

marioSprites = [[image.load("assets/sprites/mario/smallmario"+str(i)+".png").convert_alpha() for i in range(1,5)],
             [image.load("assets/sprites/mario/bigmario"+str(i)+".png").convert_alpha() for i in range(1,5)],
                [image.load("assets/sprites/mario/"+str(i)+".png").convert_alpha() for i in marioSpriteNames],
                [image.load("assets/sprites/mario/"+str(i)+".png").convert_alpha() for i in marioSpriteNamesFlag]]

brickSprites=[[image.load("assets/sprites/bricks/question"+str(i)+".png").convert_alpha() for i in range(3,0,-1)],
              [image.load("assets/sprites/bricks/brick.png").convert_alpha(),
               image.load("assets/sprites/bricks/blockidle.png").convert_alpha()]]

brickPiece = transform.scale(image.load("assets/sprites/bricks/brickpiece.png").convert_alpha(), (21,21))

statCoin = [image.load("assets/sprites/title/coin"+str(i)+".png").convert_alpha() for i in range(3,0,-1)]

coinsPic = [[image.load("assets/sprites/coins/coinidle"+str(i)+".png").convert_alpha() for i in range(3,0,-1)],
            [image.load("assets/sprites/coins/coinmove"+str(i)+".png").convert_alpha() for i in range(1,5)]]

itemsPic = [image.load("assets/sprites/items/mushroom.png").convert_alpha()]

enemiesPic = [[transform.scale(image.load("assets/sprites/enemies/goomba"+str(i)+".png").convert_alpha(), (42,42)) for i in range(1,4)],
              [transform.scale(image.load("assets/sprites/enemies/bulletbill.png").convert_alpha(),(48,42)),
               transform.scale(image.load("assets/sprites/enemies/bulletgun.png").convert_alpha(),(42,81)),
               transform.scale(image.load("assets/sprites/enemies/bulletgunext.png").convert_alpha(),(42,45))],
              [transform.scale(image.load("assets/sprites/enemies/spiny"+str(i)+".png").convert_alpha(),(42,42)) for i in range(1,3)]]

flagPic = [transform.scale(image.load("assets/sprites/items/flagpole.png").convert_alpha(), (42, 420)),
           transform.scale(image.load("assets/sprites/items/flag.png").convert_alpha(), (42, 42))]

# Resizing, Flipping, and Reordering Pictures
statCoin = [transform.scale(pic, (15,24)) for pic in statCoin]
statCoin = statCoin + statCoin[::-1]
for subList in range(len(marioSprites)):
    for pic in range(len(marioSprites[subList])):
        if marioSprites[subList][pic].get_height() == 16:
            marioSprites[subList][pic] = transform.scale(marioSprites[subList][pic], (42, 42))
        else:
            marioSprites[subList][pic] = transform.scale(marioSprites[subList][pic], (42, 84))
marioSprites[3][4], marioSprites[3][5] = transform.flip(marioSprites[3][4], True, False), transform.flip(marioSprites[3][5], True, False)


for subList in range(len(brickSprites)):
    for pic in range(len(brickSprites[subList])):
        brickSprites[subList][pic] = transform.scale(brickSprites[subList][pic], (42,42))
brickSprites[0] = brickSprites[0] + brickSprites[0][::-1]
brickPiece = [transform.flip(brickPiece, False, True),
              brickPiece,
              transform.flip(brickPiece, True, True),
              transform.flip(brickPiece, True, False)]
for subList in range(len(coinsPic)):
    for pic in range(len(coinsPic[subList])):
        coinsPic[subList][pic] = transform.scale(coinsPic[subList][pic], (30,36))
for pic in range(len(itemsPic)):
    itemsPic[pic] = transform.scale(itemsPic[pic], (42,42))
coinsPic[0] = coinsPic[0] + coinsPic[0][::-1]


# Declaring all fonts

marioFontThin = font.Font("assets/fonts/marioFont.ttf", 12)
marioFont = font.Font("assets/fonts/marioFont.ttf", 18)
marioFontBig = font.Font("assets/fonts/marioFont.ttf", 22)
marioFontSuperBig = font.Font("assets/fonts/marioFont.ttf", 30)

# Creating text

playText = marioFont.render("play", False, WHITE)
instructText = marioFont.render("instructions", False, WHITE)
creditText = marioFont.render("credits", False, WHITE)
quitText = marioFont.render("quit", False, WHITE)
pauseText = marioFont.render("paused", False, WHITE)
helpText = marioFont.render("press esc to exit game", False, WHITE)
marioText = marioFontBig.render("mario", False, WHITE)
timeText = marioFontBig.render("time", False, WHITE)
worldText = marioFontBig.render("world", False, WHITE)
overText = marioFontBig.render("Game over", False, WHITE)

instructHelp = marioFontSuperBig.render("Instructions", False, WHITE)
moveRightHelp = marioFont.render("Move Right  -  D", False, WHITE)
moveLeftHelp = marioFont.render("Move Left  -  A", False, WHITE)
jumpHelp = marioFont.render("Jump  -  Space", False, WHITE)
crouchHelp = marioFont.render("Crouch/Fast Fall  -  S", False, WHITE)
pauseHelp = marioFont.render("Pause  -  P", False, WHITE)
musicPauseHelp = marioFont.render("Mute/Unmute Music  -  M", False, WHITE)
backTextHelp = marioFont.render("Back",False,WHITE)

creditTitleHelp = marioFontSuperBig.render("Game Created By: ",False,WHITE)
creditTextHelp1 = marioFont.render("Armaan Randhawa",False,WHITE)
creditTextHelp2 = marioFont.render("Kevin Cui",False,WHITE)
creditTextHelp3 = marioFont.render("Henry Zhang",False,WHITE)

winText1 = marioFont.render("Thank You Mario!",False,WHITE)
winText2 = marioFont.render("Your quest is now over.",False,WHITE)
winText3 = marioFont.render("We present you a new quest.",False,WHITE)
winText4 = marioFont.render("Press Enter to return to menu.",False,WHITE)


# Loading all sound files

pauseSound = mixer.Sound("assets/music/effects/pause.wav")
backgroundSound = mixer.Sound("assets/music/songs/mainSong.ogg")
backgroundFastSound = mixer.Sound("assets/music/songs/mainSongFast.ogg")
deathSound = mixer.Sound("assets/music/songs/death.wav")
flagSound = mixer.Sound("assets/music/songs/flag.wav")
doneSound = mixer.Sound("assets/music/songs/leveldone.wav")
doneworldSound = mixer.Sound("assets/music/songs/worlddone.wav")
gameDoneSound = mixer.Sound("assets/music/songs/gamedone.ogg")
timepointsSound = mixer.Sound("assets/music/songs/timepoints.ogg")
overSound = mixer.Sound("assets/music/songs/gameover.ogg")
timeLowSound = mixer.Sound("assets/music/effects/timeLow.wav")
smallJumpSound = mixer.Sound("assets/music/effects/smallJump.ogg")
bigJumpSound = mixer.Sound("assets/music/effects/bigJump.ogg")
bumpSound = mixer.Sound("assets/music/effects/bump.ogg")
breakSound = mixer.Sound("assets/music/effects/brickBreak.ogg")
coinSound = mixer.Sound("assets/music/effects/coin.ogg")
appearSound = mixer.Sound("assets/music/effects/itemAppear.ogg")
stompSound = mixer.Sound("assets/music/effects/stomp.ogg")
growSound = mixer.Sound("assets/music/effects/grow.ogg")
shrinkSound = mixer.Sound("assets/music/effects/shrink.ogg")
shootSound = mixer.Sound("assets/music/effects/shoot.wav")


# Declaring game functions
def drawScene(background, backX, mario, marioPic, marioFrame, rectList, breakingBrick, brickPic, coins, moveCoins, coinsPic, mushrooms, itemsPic, enemiesList, enemiesPic, bullets, spriteCount, points, isMuted):
    """Function to draw the background, mario, enemies, and all objects"""
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    ONGROUND, JUMPFRAMES, INGROUND, ISCROUCH, ONPLATFORM, ISFALLING, ISANIMATING, INVULFRAMES = 0, 1, 2, 3, 4, 5, 6, 7
    BRICKVY, IDLE, TYPE = 4, 5, 6
    ENMYVX, ENMYVY, ENMYIDLE, ENMYINFLOOR = 4, 5, 6, 7
    GUNSTATE, GUNCOUNT, GUNTYPE = 4, 5, 6
    BULLVX, BULLVY = 4, 5
    screen.fill(BLACK) # Clearing screen
    screen.blit(background, (backX, 0))  # Blitting background
    # Blitting moving coins
    for coin in moveCoins:  # Going through each coin and defining rects
        coinRect = coin[0], coin[1], coin[2], coin[3]
        screen.blit(coinsPic[1][int(spriteCount // 0.4 % 4)], coinRect)
    # Blitting mushrooms
    for mushroom in mushrooms:  # Going through each mushroom and defining rects
        mushRect = Rect(mushroom[0], mushroom[1], mushroom[2], mushroom[3])
        if mushroom[4] == 0:  # Checkiong if the moving up animation is done
            screen.blit(itemsPic[0], mushRect)
    # Blitting enemies
    for list in enemiesList:  # For each type of enemy in the enemies list
        for enemy in list:  # For each individual enemy within that type
            enmyRect = Rect(enemy[0], enemy[1], enemy[2], enemy[3])
            if list == goombas:
                if enemy[ENMYIDLE] == 2:  # Checking if enemy is dying
                    screen.blit(enemiesPic[0][2], enmyRect)
                else:  # Normal animation
                    screen.blit(enemiesPic[0][int(spriteCount//6)], enmyRect)
            elif list == spinys:  # Same thing as goombas except with spinys
                spinePic = enemiesPic[2][int(spriteCount// 2.4 % 2)]
                if enemy[ENMYVX] > 0:  # Checking which direction the enemy is moving (1 or -1)
                    spinePic = transform.flip(spinePic, True, False)
                screen.blit(spinePic, enmyRect)
    # Blitting bricks and guns
    for list in rectList:  # For each type of bricks
        for brick in list:  # For each individual brick within that type of brick
            brickRect = Rect(brick[0], brick[1], brick[2], brick[3])  # Defining the rect of that brick
            if list == interactBricks:  # Bliting the correct picture if it is an interactBrick
                screen.blit(brickPic[1][0],brickRect)
            elif list == questionBricks:  # Doing the same thing but also checking if the brick has been hit or not
                if brick[IDLE] == 1:
                    screen.blit(brickPic[1][1], brickRect)
                else:
                    screen.blit(brickPic[0][int(spriteCount//2)],brickRect)
            elif list == gunRects:  # Bliting the pictures for the bullet bills
                if brick[GUNTYPE] == 1:
                    screen.blit(enemiesPic[1][1], (brickRect.x, brickRect.y))
                elif brick[GUNTYPE] == 2:
                    screen.blit(enemiesPic[1][2], (brickRect.x, brickRect.y))
    # Blitting brick debris
    for brick in breakingBrick: # For each break in all breakable bricks making the debris fall out in all 4 directions if broken
        screen.blit(brickPiece[0], (brick[0] - brick[5], brick[1]))
        screen.blit(brickPiece[1], (brick[0] + 21 + brick[5], brick[1]))
        screen.blit(brickPiece[2], (brick[0] - brick[5] / 2, brick[1] + 21))
        screen.blit(brickPiece[3], (brick[0] + 21 + brick[5] / 2, brick[1] + 21))
    # Blitting coins
    for coin in coins:  # For each coin in the list of all coins
        coinRect = coin[0], coin[1], coin[2], coin[3]  # Defining the coins rect
        screen.blit(coinsPic[0][int(spriteCount // 2)], coinRect)  # Bliting the coins sprite
    # Blitting bullet bills
    for bullet in bullets: # going through each bullet and defining the bullets rect
        bullRect = Rect(bullet[0], bullet[1], bullet[2], bullet[3])
        bullPic = enemiesPic[1][0]
        if bullet[BULLVX] > 0:
            bullPic = transform.flip(bullPic, True, False)
        screen.blit(bullPic, bullRect)
    # Blitting flag
    screen.blit(flagPic[0],(flagInfo[0][0],flagInfo[0][1]))  # Blitting pole
    screen.blit(flagPic[1],(flagInfo[1][0],flagInfo[1][1]))  # Blitting flag
    # Blitting mario
    marioShow = marioPic[marioFrame[0]][int(marioFrame[1])]
    if mario[DIR] == "Left":
        marioShow = transform.flip(marioShow, True, False)  # Flipping mario's sprite if he's facing left
    if marioStats[INVULFRAMES]%2 == 0 or marioStats[ISANIMATING]:  # Checking if mario's sprite should be skipped this frame
        screen.blit(marioShow, (mario[0], mario[1]))  # Blitting mario's sprite
    # Blitting floating points
    for point in points:
        pointText = marioFontThin.render("%s" %point[3], False, WHITE)  # Rendering the text
        screen.blit(pointText, (point[0], point[1]))
    # Blitting mute icon
    if isMuted:
        screen.blit(mutePic, (735,25))


def moveBricks(questionBricks, interactBricks, breakingBrick):
    """ Function to move all of the bricks when they're in the process of getting hit """
    BRICKVY, IDLE, TYPE = 4, 5, 6
    # Moving all question blocks that are hit
    for brick in questionBricks:  # Going through each question block
        if brick[BRICKVY] != 3.5 and brick[IDLE] == 1:  # Checking if the block is back at its original position or idle
            brick[BRICKVY] += 0.5  # Adding VY
            brick[1] += brick[BRICKVY]  # Applying gravity
    # Moving all bricks that are hit and resetting them after
    for brick in interactBricks:
        if brick[BRICKVY] != 3.5 and brick[IDLE] == 1:
            brick[BRICKVY] += 0.5
            brick[1] += brick[BRICKVY]
        else:  # Resetting the brick
            brick[BRICKVY] = 0
            brick[IDLE] = 0
    # Moving all brick debris
    for brick in breakingBrick:  # Going through all of the debris and adding gravity/motion
        brick[1] += brick[4]
        brick[4] += 0.8
        brick[5] += 3


def floatObjects(moveCoins, points):
    """ Function to allow coins and points to float up """
    X, Y, COINVY = 0, 1, 4
    PTSCOUNT, PTSNUM = 2, 3
    for coin in range(len(moveCoins) - 1, -1, -1): # Going through each moving coin
        if moveCoins[coin][COINVY] != 5:  # Checking if the animation is still going by checking VY
            moveCoins[coin][COINVY] += 0.5  # Adding to the VY
            moveCoins[coin][Y] += moveCoins[coin][COINVY]  # Applying gravity/VY
        else:  # Deleting coin and adding to points if the animation is finished
            points.append([moveCoins[coin][X], moveCoins[coin][Y], 30, 200])
            del moveCoins[coin]
    for point in range(len(points) - 1, -1, -1):  # Going through all points
        points[point][PTSCOUNT] -= 1  # Reducing the animation counter
        points[point][Y] -= 1  # Moving the text up


def moveItems(rectList, enemiesList, mushrooms, goombas, spinys):
    """ Function to check item/enemy collision with the environment and progress animations """
    X, Y, DELAY, MOVEUP, MUSHVX, MUSHVY, INFLOOR = 0, 1, 4, 5, 6, 7, 8
    ENMYVX, ENMYVY, ENMYIDLE, ENMYINFLOOR = 4, 5, 6, 7
    # Making sure all mushrooms are activated
    for mushroom in mushrooms:  # Going through each mushroom
        if mushroom[DELAY] > 0:  # Checking if it's being delayed and progressing the counter
            mushroom[DELAY] -= 1
        elif mushroom[MOVEUP] > 0:  # Checking if it's animating and progressing the animation
            mushroom[MOVEUP] -= 1
            mushroom[1] -= 1
        else:  # If delay and animation are done, check for its collision
            itemCollide(mushroom, rectList, [X, Y, MUSHVX, MUSHVY, INFLOOR])
    for goomba in goombas:  # Going through each goomba
        if goomba[ENMYIDLE] == 1:  # Checking if the goomba is active
            itemCollide(goomba, rectList, [X, Y, ENMYVX, ENMYVY, ENMYINFLOOR], enemiesList[:2])  # Checking collision
        if goomba[ENMYIDLE] == 2:  # Checking if the goomba is dying
            goomba[ENMYINFLOOR] -=1  # Using the INFLOOR as a counter for removal
    for spiny in spinys:  # Going through each spiny
        if spiny[ENMYIDLE] == 1:  # Checking if it's active
            itemCollide(spiny, rectList, [X, Y, ENMYVX, ENMYVY, ENMYINFLOOR], enemiesList[:2])  # Checking collision


def itemCollide(item, rectList, indexList, extraCollideIn = None):
    """ Function to check item/enemy collision with the floor, objects, and optionally other enemies """
    X, Y, VX, VY, INFLOOR = indexList[0], indexList[1], indexList[2], indexList[3], indexList[4]
    ENMYVX, ENMYVY, ENMYIDLE, ENMYINFLOOR = 4, 5, 6, 7
    extraCollide = copy.deepcopy(extraCollideIn)  # Deepcopying to remove mutability
    if extraCollide != None:  # Checking if there was an input of other rects to collide against
        for list in range(len(extraCollide)):  # Loop to remove the item itself from the rects to check against
            if item in extraCollide[list]:
                del extraCollide[list][extraCollide[list].index(item)]
        rectList = rectList + extraCollide  # Joining the two lists together
    # Applying gravity and moving the item across the screen
    item[X] += item[VX]
    item[VY] += 0.6
    item[Y] += item[VY]
    itemRect = Rect(item[0] + 3, item[1], item[2] - 3, item[3])  # Declaring rect
    # Checking collision with floor and keeping it up
    if item[Y] > 496 and not item[INFLOOR]:  # If the item is in the floor and not falling through a gap, put it back
        item[Y] = 496
        item[VY] = 0
        try:  # Checking if the item is over a gap (using colour collision) and needs to fall
            if itemRect.x > 0 and screen.get_at((itemRect.x, itemRect.bottom)) == SKYBLUE and screen.get_at((itemRect.right, itemRect.bottom)) == SKYBLUE:
                item[INFLOOR] = True
        except IndexError:  # If the item is off-screen and an IndexError is raised, ignore
            pass
    # Floor recovery code
    try:  # Checking if the item is supposed to be falling but there isn't a gap under them, and stopping their fall
        if item[INFLOOR] and screen.get_at((itemRect.x, itemRect.bottom)) != SKYBLUE and screen.get_at((itemRect.right, itemRect.bottom)) != SKYBLUE:
            item[INFLOOR] = False
    except IndexError:  # If the item is off-screen and an IndexError is raised, ignore
        pass
    itemRect = Rect(item[0], item[1], item[2], item[3])  # Re-declaring react after possible changes
    # Going through each rect in the 2D List
    for list in rectList:
        for brick in list:
            brickRect = Rect(brick[0], brick[1], brick[2], brick[3])  # Declaring rect to check against
            if itemRect.colliderect(brickRect) and itemRect != brickRect:  # Checking the two rects are colliding and that they are not the same (shouldn't collide with itself)
                if int(item[Y]) < brickRect.y:  # If the item is above the rect, put it on top (imprecise since it's not needed to be)
                    item[Y] = brickRect.y - 42
                    item[VY] = 0
                else:  # Otherwise change the direction of the item movement (allow it to bounce off)
                    # Try and except statement to skip the collision if it's a dead enemy
                    try:
                        if brick[ENMYIDLE] != 2:  # Idle state 2 means dead enemy
                            item[VX] *= -1
                    except IndexError:  # If an IndexError is raised, it means it isn't an enemy and collison should work
                        item[VX] *= -1

def shootBullets(gunRects, bullets, mario):
    """ Function to shoot bullets and to move them across the screen """
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    GUNSTATE, GUNCOUNT, GUNTYPE = 4, 5, 6
    BULLVX, BULLVY = 4, 5
    for gun in gunRects:  # Going through each gun
        if gun[GUNTYPE] == 1 and gun[GUNSTATE] == 1:  # Checking if it's the gun or just cosmetic
            gun[GUNCOUNT] += 1  # Adding to the shooting counter
            if gun[GUNCOUNT] == 180:  # If the shooting counter reaches 180
                gun[GUNCOUNT] = 0  # Reset the counter
                # Checking where Mario is and adjusting bullet stats accordingly
                bulletVX = -3
                xOffset = -48
                if mario[X] > gun[X]:
                    bulletVX = 3
                    xOffset = 42
                bullets.append([gun[X] + xOffset, gun[Y], 48, 42, bulletVX, 0])  # Append a bullet to the bullets list
                playSound(shootSound, "enemy")  # Play the bullet shooting sound
    for bullet in bullets:  # Going through each bullet
        if bullet[BULLVY] == 0:  # If the bullet has not been stepped on (Checked by seeing if it has no VY)
            bullet[X] += bullet[BULLVX]  # Move the bullet across the screen according to its VX (Negative or positive)
        else:  # If the bullet has been stepped on
            # Apply gravity
            bullet[BULLVY] += 0.6
            bullet[Y] += bullet[BULLVY]

def drawStats(mario, marioInfo, points, coins, startTime, level, fastMode, timesUp, coinPic, spriteCount, forceTime = None):
    """ Function to draw Mario's stats on screen (Points, coins, level number, and time left) """
    ONGROUND, JUMPFRAMES, INGROUND, ISCROUCH, ONPLATFORM, ISFALLING, ISANIMATING, INVULFRAMES = 0, 1, 2, 3, 4, 5, 6, 7
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    currentTime = 200 - int((time.get_ticks() - startTime) / 1000)   # Getting the time in seconds
    if forceTime != None:  # If a forced time was entered, ignore the calculated time and use the forced time
        currentTime = forceTime
    # Time checks (ignored if a forced time is entered)
    if currentTime < 100 and not fastMode and forceTime is None:  # If the time is lower than 100 and fast mode hasn't been activated
        playSound(timeLowSound, "music")  # Play the "time low" sound
        playSound(backgroundFastSound, "music", True)  # Queue the sped up background music
        fastMode = True  # Set fast mode to on
    if currentTime == 0 and not timesUp and forceTime is None:  # If the time is 0 and the times up animation hasn't been played
        currentTime = 0  # Set the current time to zero
        marioInfo[ISANIMATING] = True  # Make Mario animate
        mario[STATE] = -1  # Set his state to -1 (-1 means dead)
        timesUp = True  # Set times up to on
    # Rendering text
    points = marioFontBig.render("%06i" %int(points), False, (255,255,255))
    coins =  marioFontBig.render("x%02i" %int(coins), False, (255,255,255))
    world = marioFontBig.render("1-%i" %int(level), False, (255,255,255))
    timer = marioFontBig.render("%03i" %int(currentTime), False, (255,255,255))
    # Blitting text and coin sprite
    screen.blit(points, (75,50))
    screen.blit(marioText, (75,25))
    screen.blit(coins, (300,50))
    screen.blit(worldText, (450,25))
    screen.blit(world, (470,50))
    screen.blit(timeText, (625,25))
    screen.blit(timer, (640, 50))
    screen.blit(coinPic[int(spriteCount//2)], (275,48))
    return fastMode, timesUp  # Returning fast mode and time up values (Which could stay the same)

def drawPause():
    """ Function to draw the pause screen on top of the surface """
    alphaSurface = Surface((800, 600))  # Making a surface
    alphaSurface.set_alpha(128)  # Giving it alpha functionality
    alphaSurface.fill((0, 0, 0))  # Fill the surface with a black background
    screen.blit(alphaSurface, (0, 0))  # Blit it into the actual screen
    # Blitting pause screen text
    screen.blit(pauseText, (345,290))
    screen.blit(helpText, (210, 330))

def moveSprites(mario, marioInfo, frame, forceTime = None):
    """ Function to cycle through Mario's sprites """
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    ONGROUND, JUMPFRAMES, INGROUND, ISCROUCH, ONPLATFORM, ISFALLING, ISANIMATING, INVULFRAMES = 0, 1, 2, 3, 4, 5, 6, 7
    changingSprites = [[2,5], [2,4], [2,5], [2,4], [2,5], [2,4], [1,0]]  # List of Mario's change state sprites (Indices)
    isDead = False  # Boolean to see if the level should restart (returned and handled by game function)
    # Mario's animation loop
    if marioInfo[ISANIMATING]:  # If mario is animating
        # Animation counter checks
        if mario[STATE] == -1:  # If his state is -1 (dead)
            forceTime = 0  # Force the time to be zero
            if frame[2] > 70:  # If his animation counter has reached 70
                isDead = True  # Restart the level
        if frame[2] == 55:  # If his animation counter has reached 55
            marioInfo[ISANIMATING] = False  # Turn off his animation
            frame[2] = 0  # Reset the animation counter
            if mario[STATE] == 0:  # If his result state should be 0 (small mario)
                mario[Y] += 42  # Shift mario down
                frame[0], frame[1] = 0, 0  # Reset his sprite frame to standing
            return isDead, forceTime  # Ignore the rest of the function and return
        if mario[STATE] == -1 and frame[2] == 0:  # If mario is dying and his animation counter hasn't been touched
            frame[0], frame[1] = 2, 3  # Set his sprite to dying
            frame[2] = -15  # Turn the animation counter into a VY starting at -15
            playSound(deathSound, "music")  # Start the death music
        elif mario[STATE] == -1:  # If he's dying but his animation counter has touched (meaning above has already ran)
            frame[0], frame[1] = 2, 3  # Keep his dying sprite on
            frame[2] += 0.4  # Add to his VY
            if frame[2] > -9:  # If his VY has passed -9, then apply gravity (Acts as a delay to his falling animation)
                mario[Y] += frame[2]
        elif mario[STATE] == 0:  # If his result state should be 0 (small Mario)
            # Reverse the animation sprite List
            for index in range(len(changingSprites)):
                if changingSprites[index] == [2,5]:
                    changingSprites[index] = [1,0]
                elif changingSprites[index] == [1,0]:
                    changingSprites[index] = [2,5]
            # Add to his animation counter and apply the counter value to the current sprite
            frame[2] += 1
            frame[0], frame[1] = changingSprites[(frame[2]//8)][0], changingSprites[(frame[2]//8)][1]
        elif mario[STATE] == 1:  # Same as above but without the list reversal
            frame[2] += 1
            frame[0], frame[1] = changingSprites[(frame[2]//8)][0], changingSprites[(frame[2]//8)][1]
        return isDead, forceTime  # Stop running the function and return isDead/forceTime (Which could stay unchanged)
    # Mario's normal movement loop
    if marioInfo[ONGROUND]:
        frame[0] = 0 + mario[STATE] # Adjusting for sprite for big mario
        # Mario's running sprite counter
        if frame[1] < 3.8 and mario[VY] < 2:  # If the counter hasn't reached to upper limit and Mario isn't falling too fast
            frame[1] += mario[VX]**2/100 + 0.2  # Taking his VX and adding to counter accordingly
        else: # Mario's sprite if he's falling fast
            frame[1] = 1
        if frame[1] > 3.9:  # Sprite counter upper limit
            frame[1] = 3.9
        if mario[VX] == 0:  # If mario isn't moving, stay on his standing sprite
            frame[1] = 0
    else:
        frame[0],frame[1] = 2, 0 + mario[STATE]  # If mario is midair, stay on his jumping sprite
    if marioInfo[ISCROUCH]:
        frame[0],frame[1] = 2, 2  # If mario is crouching, stay on his crouching sprite
    if marioInfo[INVULFRAMES] != 0:  # Loop to reduce Mario's invulnerability counter
        marioInfo[INVULFRAMES] -= 1


def checkMovement(mario, marioInfo, acclerate, rectLists, pressSpace, clearRectList):
    """Function to accept inputs and apply the appropriate physics """
    keys = key.get_pressed()
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    ONGROUND, JUMPFRAMES, INGROUND, ISCROUCH, ONPLATFORM, ISFALLING, ISANIMATING = 0, 1, 2, 3, 4, 5, 6
    moving = False
    # Walking logic
    if keys[K_a] and keys[K_d]:  # If both keys are pressed, don't move
        mario[VX] = 0
    elif keys[K_a] and not marioInfo[ISCROUCH]:  # Checking if mario is hitting left side of window
        if mario[DIR] != "Left":
            mario[VX] = 0  # Stop acceleration if changing direction
        walkMario(mario, rectLists, "Left", clearRectList)
        moving = True
        mario[DIR] = "Left"
    elif keys[K_d] and not marioInfo[ISCROUCH]:
        if mario[DIR] != "Right":
            mario[VX] = 0  # Stop acceleration if changing direction
        walkMario(mario, rectLists, "Right", clearRectList)
        moving = True
        mario[DIR] = "Right"
    if keys[K_s] and mario[STATE]==1:  # Allow crouching if big mario is active
        marioInfo[ISCROUCH]=True
    if mario[STATE]==0 and marioInfo[ISCROUCH]:  # Don't allow small mario to be in crouching position
        marioInfo[ISCROUCH]=False
    if moving:  # Accelerate if there is input
        if marioInfo[ONGROUND]:
            mario[VX] += acclerate
        else:
            mario[VX] += acclerate/4  # Slow down movement when midair
    elif mario[VX] != 0:  # Move and decelerate if there is no input
        if mario[DIR] == "Right":
            walkMario(mario, rectLists, "Right", clearRectList)
        if mario[DIR] == "Left":
            walkMario(mario, rectLists, "Left", clearRectList)
        if marioInfo[ONGROUND]:  # Don't decelerate mid air
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
    if mario[STATE]==1:  # Change values if mario is big
        floor=452
        marioOffset = 88
    if marioInfo[ISCROUCH]:  # If mario is crouching, give him more gravity
        gravity = 0.9
    if marioInfo[ONPLATFORM] and mario[VY] <= gravity*2 and pressSpace:  # If mario is on a platform and pressing space, let him jump
        marioInfo[ISFALLING] = False
        marioInfo[ONPLATFORM] = False
    if keys[K_SPACE] and not marioInfo[ISCROUCH] and not marioInfo[ONPLATFORM]:
        if marioInfo[ONGROUND] and pressSpace:  # Checking if jumping is true
            mario[VY] = -9.5  # Jumping power
            marioInfo[ONGROUND] = False
            marioInfo[JUMPFRAMES] = 0
            # Playing jumping sounds
            if mario[STATE] == 0:
                playSound(smallJumpSound, "effect")
            else:
                playSound(bigJumpSound, "effect")
        elif marioInfo[JUMPFRAMES] < 41 and not marioInfo[ISFALLING] and not marioInfo[ONPLATFORM]: # Simulating higher jump with less gravity
            gravity = 0.2
            marioInfo[JUMPFRAMES] += 1
    mario[Y] += mario[VY]  # Add the y movement value
    if not marioInfo[INGROUND] and mario[Y]>=floor and screen.get_at((int(mario[X]+4),int(mario[Y]+marioOffset)))==SKYBLUE and \
       screen.get_at((int(mario[X]+38),int(mario[Y]+marioOffset)))==SKYBLUE:
        # Using colour collision to fall through holes
        marioInfo[INGROUND] = True
        marioInfo[ONGROUND] = False
    elif mario[Y] >= floor and not marioInfo[INGROUND]:  # Checking floor collision
        mario[Y] = floor  # stay on the ground
        mario[VY] = 0  # stop falling
        marioInfo[ONGROUND] = True
        marioInfo[ONPLATFORM] = False
        marioInfo[ISFALLING] = False
    # Try except statement for Mario's falling recovery
    try:
        if marioInfo[INGROUND] and screen.get_at((int(mario[X]+4),int(mario[Y]+marioOffset)))!=SKYBLUE and \
           screen.get_at((int(mario[X]+38),int(mario[Y]+marioOffset)))!=SKYBLUE: # Allow mario to recover if he goes back above the ground
            marioInfo[INGROUND] = False
    except IndexError:  # If IndexError is raised, ignore
        pass
    if marioInfo[INGROUND] and mario[Y] > 700:  # If Mario falls off the screen, play his dying animation
        marioInfo[ISANIMATING] = True  # Set animating to True
        mario[STATE] = -1  # Put his state to -1 (dead)
    marioPos[VY] += gravity  # apply gravity


def walkMario(mario, rectLists, direction, clearRectList):
    """ Function to move the player, background, and all rectangles """
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
            # Moving all rectangles
            for subList in range(len(rectLists)):
                for rect in range(len(rectLists[subList])):
                    rectLists[subList][rect][0] -= mario[VX]
            for subList in range(len(clearRectList)):
                for rect in range(len(clearRectList[subList])):
                    clearRectList[subList][rect][0] -= mario[VX]
    if mario[X] < 0:
        mario[X] = 0


def checkCollide(mario, marioInfo, marioScore, rectLists, breakingBrick, moveCoins, mushrooms):
    """ Function to check mario's collision with Rects"""
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    ONGROUND, JUMPFRAMES, INGROUND, ISCROUCH, ONPLATFORM, ISFALLING = 0, 1, 2, 3, 4, 5
    BRICKVY, IDLE, TYPE = 4, 5, 6
    PTS, COIN, LIVES = 0, 1, 2
    height = 42
    if mario[STATE] == 1:
        height = 84
    originalMarioRect = Rect(mario[X] + 2, mario[Y], 38 - 2, height)
    originalX, originalY, originalVY = mario[X], mario[Y], mario[VY]
    hitBrick = []
    for list in rectLists:
        for brick in list:
            brickRect = Rect(brick[0], brick[1], brick[2], brick[3])
            marioRect = Rect(mario[X] + 2, mario[Y], 38 - 2, height) # Mario's hit box (and making it a little smaller)
            if brickRect.colliderect(marioRect):
                if int(mario[Y]) + height - int(mario[VY]) - 1 <= brickRect.y:  # Hitting top collision
                    marioInfo[ONGROUND] = True
                    marioInfo[ONPLATFORM] = True
                    marioInfo[ISFALLING] = True
                    mario[VY] = 0
                    mario[Y] = brickRect.y - height
                elif int(mario[Y] - mario[VY]) >= int(brickRect.y + brickRect.height):  # Hitting bottom collision
                    mario[Y] -= mario[VY]
                    mario[VY] = 1
                    mario[Y] = brickRect.y + brickRect.height
                    marioInfo[JUMPFRAMES] = 41
                elif int(mario[X] + 2) >= int(brickRect[X]):  # Right side collision
                    mario[X] = brickRect.x + brickRect.width - 2  # Move mario to the right of the rect
                    mario[VX] = 0
                elif int(mario[X] + 2) <= int(brickRect[X]):  # Left side collision
                    mario[X] = brickRect.x - 38  # Move mario to the left of the rect
                    mario[VX] = 0
            if list != brickList and brickRect.colliderect(originalMarioRect) and originalY - originalVY >= brickRect.y + brickRect.height:
                hitBrick.append([brick, list])
    for list in hitBrick:
        brick, type = list[0], list[1]
        brickRect = Rect(brick[0], brick[1], brick[2], brick[3])
        # Handling collision with multiple bricks
        if len(hitBrick) != 1:
            if abs(brickRect.x - originalX) > 21:
                continue
            else:
                del hitBrick[-1]
        # Manipulating bricks appropriately
        if type == interactBricks and brick[IDLE] == 0:
            indexBrick = interactBricks.index(brick)
            if brick[TYPE] > 0 or mario[STATE] == 0:
                interactBricks[indexBrick][BRICKVY] = -4
                interactBricks[indexBrick][IDLE] = 1
                playSound(bumpSound, "effect")
                if brick[TYPE] > 0:
                    brick[TYPE] -= 1
                    moveCoins.append([interactBricks[indexBrick][0] + 6, interactBricks[indexBrick][1], 30, 32, -12])
                    playSound(coinSound, "block")
                    marioScore[COIN] += 1
                    marioScore[PTS] += 200
                    if brick[TYPE] == 0:
                        questionBricks.append([brick[0], brick[1], brick[2], brick[3], brick[4], brick[5], 0])
                        del interactBricks[indexBrick]
            else:
                interactBricks[indexBrick][BRICKVY] = -9
                breakingBrick.append(interactBricks[indexBrick])
                del interactBricks[indexBrick]
                playSound(breakSound, "block")  # Play bumping sound
        elif type == questionBricks:
            playSound(bumpSound, "effect")  # Play bumping sound
            if brick[IDLE] == 0:
                indexBrick = questionBricks.index(brick)
                questionBricks[indexBrick][IDLE] = 1
                questionBricks[indexBrick][BRICKVY] = -4
                if questionBricks[indexBrick][TYPE] == 1:
                    moveCoins.append([questionBricks[indexBrick][0] + 6, questionBricks[indexBrick][1], 30, 32, -12])
                    playSound(coinSound, "block")
                    marioScore[COIN] += 1
                    marioScore[PTS] += 200
                elif questionBricks[indexBrick][TYPE] == 2:
                    mushrooms.append([questionBricks[indexBrick][0], questionBricks[indexBrick][1], 42, 42, 15, 42, 3, 0, False])
                    playSound(appearSound, "block")


def checkClearCollide(mario, marioStats, marioScore, coins, mushrooms, enemiesList, points, bullets, startTime):
    PTS, COIN, LIVES = 0, 1, 2
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    ONGROUND, JUMPFRAMES, INGROUND, ISCROUCH, ONPLATFORM, ISFALLING, ISANIMATING, INVULFRAMES = 0, 1, 2, 3, 4, 5, 6, 7
    X, Y, DELAY, MOVEUP, MUSHVX, MUSHVY = 0, 1, 4, 5, 6, 7
    ENMYVX, ENMYVY, ENMYIDLE, ENMYINFLOOR = 4, 5, 6, 7
    BULLVX, BULLVY = 4, 5
    height = 42
    if mario[STATE] == 1:
        height = 84
    marioRect = Rect(mario[X], mario[Y], 38 - 2, height)
    if marioStats[ISCROUCH]:
        marioRect = Rect(mario[X], mario[Y] + 42, 38 - 2, 42)
    for coin in range(len(coins) - 1, -1, -1):
        coinRect = Rect(coins[coin][0], coins[coin][1], coins[coin][2], coins[coin][3])
        if marioRect.colliderect(coinRect):
            del coins[coin]
            playSound(coinSound, "block")
            marioScore[PTS] += 200
            points.append([coinRect.x, coinRect.y, 30, 200])
            marioScore[COIN] += 1
    for index in range(len(mushrooms) - 1, -1, -1):
        mushRect = Rect(mushrooms[index][0], mushrooms[index][1], mushrooms[index][2], mushrooms[index][3])
        if marioRect.colliderect(mushRect) and mushrooms[index][DELAY] == 0 and mushrooms[index][MOVEUP] == 0:
            if mario[STATE] == 0:
                mario[Y] -= 42
                mario[STATE] = 1
                marioStats[ISANIMATING] = True
                playSound(growSound, "effect")
            marioScore[PTS] += 2000
            points.append([mushRect.x, mushRect.y, 30, 2000])
            del mushrooms[index]
    for list in range(len(enemiesList)):
        for enemy in range(len(enemiesList[list]) - 1, -1, -1):
            # Defining hitbox
            if enemiesList[list] == goombas or enemiesList[list] == spinys:
                enmyRect = Rect(enemiesList[list][enemy][0] + 5, enemiesList[list][enemy][1] + 10, enemiesList[list][enemy][2] - 10, enemiesList[list][enemy][3] - 10)
            elif enemiesList[list] == bullets:
                enmyRect = Rect(enemiesList[list][enemy][0] + 15, enemiesList[list][enemy][1], enemiesList[list][enemy][2] - 15, enemiesList[list][enemy][3])
            # Checking proper collision
            if marioRect.colliderect(enmyRect) and ((enemiesList[list] == goombas and enemiesList[list][enemy][ENMYIDLE] != 2) or (enemiesList[list] == bullets and enemiesList[list][enemy][BULLVY] == 0) or (enemiesList[list] == spinys)):
                if int(mario[Y]) + height - int(mario[VY]) <= enmyRect.y and enemiesList[list] != spinys:
                    mario[VY] = -7.5
                    marioStats[ISFALLING] = True
                    marioStats[ONGROUND] = False
                    marioScore[PTS] += 100
                    playSound(stompSound, "effect")
                    if enemiesList[list] == goombas:
                        enemiesList[list][enemy][ENMYIDLE] = 2
                        enemiesList[list][enemy][ENMYINFLOOR] = 32  # Turning the infloor value into a counter for removing dead goombas
                    elif enemiesList[list] == bullets:
                        enemiesList[list][enemy][BULLVY] = -1
                        points.append([enmyRect.x, enmyRect.y, 30, 100])
                elif marioStats[INVULFRAMES] == 0:
                    mario[STATE] -= 1
                    marioStats[ISANIMATING] = True
                    if mario[STATE] == 0:
                        marioStats[INVULFRAMES] = 80
                        playSound(shrinkSound, "effect")
    # Checking victory pole collision
    isPole = False
    forceTime = None
    poleRect = Rect(flagInfo[0][0], flagInfo[0][1], flagInfo[0][2], flagInfo[0][3])
    if marioRect.colliderect(poleRect):  # If mario collides with the pole
        isPole = True
        mario[X] = poleRect.x - 16  # Making mario slide down
        playSound(flagSound, "music")  # Playing the flag sound
        forceTime = 200 - (time.get_ticks() - startTime)//1000
    return [isPole, forceTime]

def movePole(mario, marioStats, marioScore, frame, flagInfo, unisprite, isDone, forceTime):
    PTS, COIN, LIVES = 0, 1, 2
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    ONGROUND, JUMPFRAMES, INGROUND, ISCROUCH, ONPLATFORM, ISFALLING, ISANIMATING, INVULFRAMES = 0, 1, 2, 3, 4, 5, 6, 7
    poleRect = Rect(flagInfo[0][0], flagInfo[0][1], flagInfo[0][2], flagInfo[0][3])
    flagRect = Rect(flagInfo[1][0], flagInfo[1][1], flagInfo[1][2], flagInfo[1][3])
    offset = 0
    endPoint = 650
    if levelNum == 5:
        endPoint = 690
    if mario[STATE] == 1:
        offset = 42
    if flagRect.y < 451:
        flagInfo[1][1] += 4
    if mario[Y] < 451 - offset:
        mario[Y] += 4
        frame[0], frame[1] = 3, (unisprite * 0.8 % 2 + mario[STATE] * 2)
    if mario[Y] >= 451 - offset and flagRect.y >= 451 and frame[2] < 20:
        mario[X] = poleRect.x + 16
        frame[0], frame[1] = 3, 4 + mario[STATE]
        frame[2] += 1
    elif mario[Y] >= 451 - offset and flagRect.y >= 451 and frame[2] == 20:
        mario[X] = poleRect.right
        mario[Y] = 496 - offset
        frame[2] += 1
        if levelNum != 5:
            playSound(doneSound, "music")
        else:
            playSound(doneworldSound, "music")
    elif mario[Y] >= 451 - offset and flagRect.y >= 451:
        mario[VX] = 5
        mario[VY] = 0
        mario[X] += 3.5
        marioStats[ONGROUND] = True
        moveSprites(mario,marioStats,frame)
        if mario[X] > endPoint and mario[X] < 800:
            mario[X] = 800
            playSound(timepointsSound, "effect")
    if mario[X] > 800 and forceTime != 0:
        forceTime -= 1
        marioScore[PTS] += 100
    if forceTime == 0:
        mixer.Channel(1).stop()
        if not mixer.Channel(0).get_busy():
            isDone = True
    return [isDone, forceTime]

def rotateRect(rectList, breakingBrick, itemsList, enemiesList, bullets, gunsList, points):
    """ Function to take the activate and deactivate Rects relative to the screen """
    X, Y, ENMYVX, ENMYVY, ENMYIDLE, ENMYINFLOOR = 0, 1, 4, 5, 6, 7
    GUNSTATE, GUNCOUNT, GUNTYPE = 4, 5, 6
    # Deleting any offscreen Rects
    for index in range(len(breakingBrick) - 1, -1, -1):  # Going through all of the brick debris and deleting them once they exit below the screen
        if breakingBrick[index][1] > 600:
            del breakingBrick[index]
    for list in range(len(itemsList)):  # Going through all of the items and deleting them once they scroll off the screen
        for item in range(len(itemsList[list]) - 1, -1, -1):
            if itemsList[list][item][0] < -300 or itemsList[list][item][1] > 650:
                del itemsList[list][item]
    for list in range(len(rectList)):  # Going through all of the rects and deleting them once they scroll off the screen
        for rect in range(len(rectList[list]) - 1, -1, -1):
            if rectList[list][rect][0] < -700:
                del rectList[list][rect]
    for list in range(len(enemiesList)):  # Going through all of the enemies and deleting them once they scroll off the screen
        for rect in range(len(enemiesList[list]) - 1, -1, -1):
            if enemiesList[list][rect][0] < -300 or enemiesList[list][rect][1] > 650:
                del enemiesList[list][rect]
    for point in range(len(points) - 1, -1, -1):  # Going through all of the points indicators and deleting them once the counter reaches zero
        if points[point][2] == 0:
            del points[point]
    # Activating and deactivating all enemies
    for list in range(len(enemiesList)):  # Going through all of the enemies
        for enemy in range(len(enemiesList[list]) - 1, -1, -1):
            if enemiesList[list] == goombas or enemiesList[list] == spinys:  # If they are goombas or spinys
                # Activating goombas and spinys if they get close to the screen
                if enemiesList[list][enemy][ENMYIDLE] == 0 and enemiesList[list][enemy][X] < 800:
                    enemiesList[list][enemy][ENMYIDLE] = 1
                # Deleting them if they are crushed by mario and the death counter reaches zero
                elif enemiesList[list][enemy][ENMYIDLE] == 2 and enemiesList[list][enemy][ENMYINFLOOR] == 0:
                    points.append([enemiesList[list][enemy][0], enemiesList[list][enemy][1], 40, 100])
                    del enemiesList[list][enemy]
            elif enemiesList[list] == bullets:  # If they are bullets
                # Deleting bullets if they are too far off screen
                if enemiesList[list][enemy][0] < -1600 or enemiesList[list][enemy][0] > 1600:
                    del enemiesList[list][enemy]
    for gun in range(len(gunsList) - 1, -1, -1):  # Going through all of the guns
        # Activating guns if they get close and deleting them if they get too far back
        if gunsList[gun][0] < 1600:
            gunsList[gun][GUNSTATE] = 1
        if gunsList[gun][0] < -1600:
            del gunsList[gun]

def playSound(soundFile, soundChannel, queue = False):
    """ Function to load in sounds and play them on a channel """
    channelList = [["music", 0], ["effect", 1], ["block", 2], ["extra", 3], ["enemy", 4]]  # List to keep track of mixer channels
    for subList in channelList:  # For loop to identify the input through corresponding lists
        if subList[0] == soundChannel:
            channelNumber = subList[1]  # Taking the matching channel number and declaring it
    if queue:  # If the input requests for a queue
        mixer.Channel(channelNumber).queue(soundFile)  # Add the sound to the queue
    else:
        mixer.Channel(channelNumber).stop()  # Stopping any previous sound
        mixer.Channel(channelNumber).play(soundFile)  # Playing new sound

def globalSound(command):
    """ Function to apply commands to all mixer channels """
    for id in range(mixer.get_num_channels()):  # Going through each mixer channel
        if command == "stop":
            mixer.Channel(id).stop()  # Stopping all playback on the channel
        elif command == "pause":
            mixer.Channel(id).pause()  # Pausing playback on the channel
        elif command == "unpause":
            mixer.Channel(id).unpause() # Unpausing playback on the channel
        elif command == "toggleVol":
            if mixer.Channel(id).get_volume() == 0:  # Checking if the channel is muted
                mixer.Channel(id).set_volume(1)  # Unmuting the channel
            else:
                mixer.Channel(id).set_volume(0)  # Otherwise, mute the channel


def spriteCounter(counter):
    """ Function to progress the universal sprite counter"""
    counter += 0.2  # Adding to the counter
    if counter > 10:  # Checking if the counter hits the limit and resetting it
        counter = 0
    return counter  # Returning the new counter


# Declaring loading functions

def loadFile(targetFile):
    """ Function to load files and make lists out of them"""
    outputList = []
    file = open(targetFile, "r")  # Loading file
    fileLines = file.readlines()  # Splitting into lines
    for line in fileLines:
        line = line.strip("\n")  # Removing any line separators
        line = line.split(",")  # Dividing elements separated by commas
        listLength = len(line)
        outputList.append([int(line[index]) for index in range(listLength)])  # Appending line info to list
    return outputList  # Returning final list

# Declaring main functions

def game():
    """ Main game function """
    running = True
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    ONGROUND, JUMPFRAMES, INGROUND, ISCROUCH, ONPLATFORM, ISFALLING, ISANIMATING = 0, 1, 2, 3, 4, 5, 6
    PTS, COIN, LIVES = 0, 1, 2
    global levelNum, marioStats, RECTFINDER, marioPos, marioScore # REMOVE THESE AT END
    playSound(backgroundSound, "music")  # Starting the background music
    # Declaring session specific booleans
    pausedBool = False  # Boolean to keep track of pause status
    isMuted = False  # Boolean to see if the sound is muted
    if mixer.Channel(0).get_volume() == 0:  # Checking current volume and fixing mute boolean accordingly
        isMuted = True
    timesUp = False  # Boolean to see if the game timer has reached zero
    isPole = False  # Boolean to see if Mario is animating on the victory pole
    isDead = False  # Boolean to see if the game should reload the level after death
    isDone = False  # Boolean to see if the game should load the next level after victory
    fast = False  # Boolean to see if the music is playing faster
    uniSprite = 0  # Counter to control all non - Mario sprites
    forceTime = None  # Variable to keep track of a time that should be forced on screen
    # Declaring session specific lists
    breakingBrick = []  # List of bricks that are broken and showing their debris
    moveCoins = []  # List of animating coins that Mario has grabbed
    mushrooms = []  # List of mushroom powerups
    bullets = []  # List of bullet bill enemies
    points = []  # List of animating point indicators
    # Declaring packaged lists
    rectList = [brickList, interactBricks, questionBricks, gunRects]  # List of rectangles Mario can't pass through
    clearRectList = [coins, moveCoins, breakingBrick, mushrooms, goombas, points, flagInfo, bullets, spinys]  # List of rectangles Mario can pass through
    itemsList = [mushrooms]  # List of all items
    enemiesList = [goombas, spinys, bullets]  # List of all enemies
    startTime = time.get_ticks()  # Variable to keep track of time since level start
    while running:
        mx, my = mouse.get_pos()
        initialSpace = False
        for evnt in event.get():
            if evnt.type == QUIT:
                return "exit"
            if evnt.type == KEYDOWN:
                # Keep track of when the user first presses space
                if evnt.key == K_SPACE:
                    initialSpace = True
                # Toggling the music volume on or off
                elif evnt.key == K_m:
                    isMuted = not isMuted
                    globalSound("toggleVol")
                # Toggling the paused status
                elif evnt.key == K_p:
                    pausedBool = not pausedBool
                    if pausedBool:
                        globalSound("pause")
                        playSound(pauseSound, "extra")
                        pauseTime = time.get_ticks() - startTime
                    else:
                        globalSound("unpause")
                # Exiting the game
                elif evnt.key == K_ESCAPE and pausedBool:
                    return "menu"
            elif evnt.type == KEYUP:
                # Keep track of when user lets go of space
                if evnt.key == K_SPACE:
                    marioStats[ISFALLING] = True
                # Keep track of when user lets go of the crouch key
                elif evnt.key== K_s:
                    marioStats[ISCROUCH]=False
        # Functions to run during normal play
        if not pausedBool and not marioStats[ISANIMATING] and not isPole:  # If the game isn't paused, Mario isn't animating, and Mario isn't on the flag pole
            uniSprite = spriteCounter(uniSprite)
            rotateRect(rectList, breakingBrick, itemsList, enemiesList, bullets, gunRects, points)
            checkMovement(marioPos, marioStats, marioAccelerate, rectList, initialSpace, clearRectList)
            moveSprites(marioPos, marioStats, marioFrame)
            moveBricks(questionBricks, interactBricks, breakingBrick)
            floatObjects(moveCoins, points)
            moveItems(rectList, enemiesList, mushrooms, goombas, spinys)
            shootBullets(gunRects, bullets, marioPos)
            checkCollide(marioPos, marioStats, marioScore, rectList, breakingBrick, moveCoins, mushrooms)
            isPole, forceTime = checkClearCollide(marioPos, marioStats, marioScore, coins, mushrooms, enemiesList, points, bullets, startTime)
        # Functions to run during Mario animations
        if marioStats[ISANIMATING]:  # If Mario is animating
            isDead, forceTime = moveSprites(marioPos, marioStats, marioFrame, forceTime)
        # Functions to run during Mario's end of level animation
        if isPole and not pausedBool:  # If Mario is on the flag pole and the game isn't paused
            fast = True
            uniSprite = spriteCounter(uniSprite)
            isDone, forceTime = movePole(marioPos, marioStats, marioScore, marioFrame, flagInfo, uniSprite, isDone, forceTime)
        # Drawing the scene
        drawScene(backgroundPics[levelNum - 1], backPos, marioPos, marioSprites, marioFrame, rectList, breakingBrick, brickSprites, coins, moveCoins, coinsPic, mushrooms, itemsPic, enemiesList, enemiesPic, bullets, uniSprite, points, isMuted)
        fast, timesUp = drawStats(marioPos, marioStats, marioScore[PTS], marioScore[COIN], startTime, levelNum, fast, timesUp, statCoin, uniSprite, forceTime)
        # Functions to run during paused state
        if pausedBool:
            drawPause()
            startTime += (time.get_ticks() - startTime) - pauseTime
        # Updating the display
        display.flip()
        fpsCounter.tick(60)
        display.set_caption("Super Mario Bros! FPS: %.2f" %fpsCounter.get_fps())
        # End of game handling
        if isDead:  # If Mario died
            levelNum -= 1  # Adjust the level number so it loads the same level
            marioScore[LIVES] -= 1  # Reduce the number of lives
            if marioScore[LIVES] == 0:  # If Mario has zero lives left, go to the game over screen
                return "gameOver"
            return "loading"
        if isDone:  # If Mario reached the end of the level
            if levelNum == 5:  # If the current level is 5, load the win screen
                return "win"
            return "loading"

def menu(selected):
    """ Function to reset all game variables and display the menu screen """
    global levelNum, marioScore
    # Resetting volume and game variables
    if mixer.Channel(0).get_volume() == 0:
        globalSound("toggleVol")
    levelNum = 0
    marioScore= [0, 0, 5]
    running = True
    globalSound("stop") # Stop any music that's playing
    # Menu screen corresponding lists
    textPoints = [[360, 350], [290, 390], [333, 430], [360, 470]]
    textList = [playText, instructText, creditText, quitText]
    returnList = ["loading", "instructions", "credit", "exit"]
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                return ["exit", None]
            if evnt.type == KEYDOWN:
                # Checking for menu screen inputs
                if evnt.key == K_UP or evnt.key == K_w:  # Making the cursor go up
                    selected -= 1
                elif evnt.key == K_DOWN or evnt.key == K_s:  # Making the cursor go down
                    selected += 1
                elif evnt.key == K_RETURN:  # Selecting an option
                    return [returnList[selected], selected]
        # Keeping the cursor within the bounds of the options
        if selected < 0:
            selected = 3
        elif selected > 3:
            selected = 0
        # Drawing the background and buttons
        screen.blit(backgroundPics[0],(0,0))  # Blitting background
        screen.blit(marioSprites[0][0], (40, 496))  # Blitting Mario
        screen.blit(titleLogo,(160,80))  # Blitting title
        for index in range(len(textList)):  # Go through all of the menu text and blit it at the corresponding coordinates
            screen.blit(textList[index], (textPoints[index][0], textPoints[index][1]))
        screen.blit(titleSelect, (textPoints[selected][0] - 30, textPoints[selected][1] - 4 ))  # Blitting the selected option icon
        display.flip()
        fpsCounter.tick(60)
    return ["exit", selected]


def loading():
    """ Function to load in all game objects, prepare variables, and to display loading screen """
    PTS, COIN, LIVES = 0, 1, 2
    # Loading up and declaring all level elements
    global levelNum, marioPos
    globalSound("stop") # Stopping all music
    # Preparing game variables for next level
    levelNum += 1
    oldState = marioPos[5]
    if oldState == -1:
        oldState = 0
    marioPos = [40, 496, 0, 0, "Right", oldState]
    marioStats = [True, 0, False, False, False, False, False, 0]
    backPos = 0
    marioFrame = [0,0, 0]
    # Loading in all level objects
    brickList = loadFile(str("data/level_" + str(levelNum) + "/bricks.txt"))
    interactBricks = loadFile(str("data/level_" + str(levelNum) + "/interactBricks.txt"))  # 1-4: Rect, VY, State, Coins
    questionBricks = loadFile(str("data/level_" + str(levelNum) + "/questionBricks.txt"))  # 1-4: Rect, VY, State, Type
    coins = loadFile(str("data/level_" + str(levelNum) + "/coins.txt"))
    goombas = loadFile(str("data/level_" + str(levelNum) + "/goombas.txt"))
    spinys = loadFile(str("data/level_" + str(levelNum) + "/spinys.txt"))
    gunRects = loadFile(str("data/level_" + str(levelNum) + "/guns.txt"))
    flagInfo = loadFile(str("data/level_" + str(levelNum) + "/flag.txt"))
    # Loading screen variables and rendered text
    uniSprite = 0
    currentWorld = marioFontBig.render("World 1-%s" %levelNum, False, (255,255,255))
    lives = marioFontBig.render("X  %s" %marioScore[LIVES], False, (255,255,255))
    startTime = time.get_ticks()
    # Menu screen that should only stay for 2.5 seconds
    while time.get_ticks() - startTime < 2500:
        for evnt in event.get():          
            if evnt.type == QUIT:
                return ["exit", None, None, None, None, None, None, None, None, None, None, None, None]
        # Drawing loading screen
        screen.fill(BLACK)  # Clearing screen
        uniSprite = spriteCounter(uniSprite)  # Progressing the sprites
        drawStats(None, None, marioScore[PTS], marioScore[COIN], time.get_ticks(), levelNum, True, True, statCoin, uniSprite)
        screen.blit(currentWorld, (300, 250))  # Blitting current world text
        screen.blit(lives, (390, 315))  # Blitting number of lives text
        screen.blit(marioSprites[0][0], (315, 300))  # Blitting mario
        display.flip()
        fpsCounter.tick(60)
    # Returning all variables for game function to handle
    return ["game", brickList, interactBricks, questionBricks, coins, goombas, flagInfo, marioPos, backPos, marioStats, marioFrame, gunRects, spinys]

def gameOver():
    """ Function to display game over screen """
    PTS, COIN, LIVES = 0, 1, 2
    uniSprite = 0
    globalSound("stop") # Stopping any music
    playSound(overSound, "music") # Playing game over music
    startTime = time.get_ticks()
    # Game over screen should only stay for 5 seconds
    while time.get_ticks() - startTime < 5000:
        for evnt in event.get():
            if evnt.type == QUIT:
                return "exit"
        # Drawing game over screen
        screen.fill(BLACK)
        uniSprite = spriteCounter(uniSprite)
        drawStats(None, None, marioScore[PTS], marioScore[COIN], time.get_ticks(), levelNum, True, True, statCoin,
                  uniSprite, 0)
        screen.blit(overText,(300,300))  # Blitting game over text
        display.flip()
        fpsCounter.tick(60)
    return "menu"

def win(marioPos):
    """ Function to display winning screen"""
    PTS, COIN, LIVES = 0, 1, 2
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    globalSound("stop") # Stopping any music
    playSound(gameDoneSound, "music") # Playing win music
    # Adjusting Mario position depending on his state
    if marioPos[STATE] == 0:  # If he's small
        marioPos = [-50, 495, 5, 0, "Right", 0]
    else:  # If he's big
        marioPos = [-50, 451, 5, 0, "Right", 1]
    frame = [0,0,0]
    canExit = False  # Boolean to check if user can press enter and exit win screen
    startTime = None  # Variable to keep track of time since text starts to appear
    running = True
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                return "exit"
            elif evnt.type == KEYDOWN:
                if evnt.key == K_RETURN and canExit:  # If the user has pressed Enter and is allowed to exit, return to the menu
                    return "menu"
        # Moving Mario
        if marioPos[X] < 350:  # Moving him if he's not in the right place
            marioPos[X] += 5
        elif startTime == None:  # If we don't need to move Mario and a text time hasn't been established yet
            startTime = time.get_ticks()  # Get the current time
            marioPos[VX] = 0  # Stop mario's moving animation by removing his speed
        moveSprites(marioPos, marioStats, frame, 0)  # Animating mario
        # Drawing win screen
        screen.fill(BLACK)  # Clearing screen
        screen.blit(winPics[0], (0, 0))  # Blitting the background
        screen.blit(winPics[1], (430, 467))  # Blitting peach sprite
        screen.blit(marioSprites[frame[0]][int(frame[1])], (marioPos[X], marioPos[Y]))  # Blitting Mario
        # Checking for text times and drawing text
        if startTime != None:  # If a text time has been established
            timeDiff = time.get_ticks() - startTime  # Calculate the time that has passed
            screen.blit(winText1, (250,170))  # Always blit the first line
            if timeDiff > 2000:
                screen.blit(winText2, (190, 260))  # Blit this if 2s have passed
            if timeDiff > 4000:
                screen.blit(winText3, (160, 300))  # Blit this if 4s have passed
            if timeDiff > 6000:
                screen.blit(winText4, (135, 390))  # Blit this if 6s have passed
                canExit = True  # Allow the user to exit
        display.flip()
        fpsCounter.tick(60)
    return "menu"

def instructions():
    """ Function to display instructions screen """
    running = True
    while running:
        for evnt in event.get():
            if evnt.type == KEYDOWN:
                if evnt.key == K_RETURN:
                    return "menu"
            if evnt.type == QUIT:
                return "exit"
        # Drawing all of the instructions screen text and background
        screen.blit(backgroundPics[0],(0,0))
        screen.blit(instructHelp,(235,40))
        screen.blit(moveRightHelp,(80,130))
        screen.blit(moveLeftHelp,(80,170))
        screen.blit(jumpHelp,(80,210))
        screen.blit(crouchHelp,(80,250))
        screen.blit(pauseHelp,(80,290))
        screen.blit(musicPauseHelp,(80,330))
        screen.blit(backTextHelp,(650,450))
        screen.blit(titleSelect,(610,445))
        screen.blit(brickSprites[0][3], (375,400))
        display.flip()
        fpsCounter.tick(60)
    return "menu"


def credit():
    """ Function to display credits screen """
    running = True
    while running:
        for evnt in event.get():
            if evnt.type == KEYDOWN:
                if evnt.key == K_RETURN:
                    return "menu"
            if evnt.type == QUIT:
                return "exit"
        # Drawing background and text
        screen.blit(backgroundPics[0], (0, 0))
        screen.blit(creditTitleHelp,(170,45))
        screen.blit(marioSprites[0][0],(400,494))
        screen.blit(marioSprites[1][0],(130,452))
        screen.blit(enemiesPic[0][0],(630,495))
        screen.blit(creditTextHelp1,(30,350))
        screen.blit(creditTextHelp2, (335, 400))
        screen.blit(creditTextHelp3, (550, 440))
        screen.blit(backTextHelp, (50, 50))
        screen.blit(titleSelect, (10, 45))
        display.flip()
        fpsCounter.tick(60)
    return "menu"

# Main loop to check for which page to fall on
while page != "exit":
    if page == "menu":
        page, selected = menu(selected)
    if page == "loading":
        page, brickList, interactBricks, questionBricks, coins, goombas, flagInfo, marioPos, backPos, marioStats, marioFrame, gunRects, spinys = loading()
    if page == "gameOver":
        page = gameOver()
    if page == "win":
        page = win(marioPos)
    if page == "game":
        page = game()
    if page == "instructions":
        page = instructions()     
    if page == "credit":
        page = credit()
quit()