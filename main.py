from pygame import *
from random import *
import copy
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

# Declaring Variables
page = "menu"
fpsCounter = time.Clock()
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
marioAccelerate = 0.2  # The value at which mario can speed up and slow down
backPos = 0  # Position of the background
levelNum = 0  # Using 0 as level 1 since indexes start at 0
selected = 0  # Variable for current selected option in menu

RECTFINDER = [0,0] #DELETE THIS LATER
    
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
    for coin in moveCoins:
        coinRect = coin[0], coin[1], coin[2], coin[3]
        screen.blit(coinsPic[1][int(spriteCount // 0.4 % 4)], coinRect)
    # Blitting mushrooms
    for mushroom in mushrooms:
        mushRect = Rect(mushroom[0], mushroom[1], mushroom[2], mushroom[3])
        if mushroom[4] == 0:
            screen.blit(itemsPic[0], mushRect)
    # Blitting enemies
    for list in enemiesList:
        for enemy in list:
            enmyRect = Rect(enemy[0], enemy[1], enemy[2], enemy[3])
            if list == goombas:
                if enemy[ENMYIDLE] == 2:
                    screen.blit(enemiesPic[0][2], enmyRect)
                else:
                    screen.blit(enemiesPic[0][int(spriteCount//6)], enmyRect)
            elif list == spinys:
                spinePic = enemiesPic[2][int(spriteCount// 2.4 % 2)]
                if enemy[ENMYVX] > 0:
                    spinePic = transform.flip(spinePic, True, False)
                screen.blit(spinePic, enmyRect)
    # Blitting bricks and guns
    for list in rectList:
        for brick in list:
            brickRect = Rect(brick[0], brick[1], brick[2], brick[3])
            if list == interactBricks:
                screen.blit(brickPic[1][0],brickRect)
            elif list == questionBricks:
                if brick[IDLE] == 1:
                    screen.blit(brickPic[1][1], brickRect)
                else:
                    screen.blit(brickPic[0][int(spriteCount//2)],brickRect)
            elif list == gunRects:
                if brick[GUNTYPE] == 1:
                    screen.blit(enemiesPic[1][1], (brickRect.x, brickRect.y))
                elif brick[GUNTYPE] == 2:
                    screen.blit(enemiesPic[1][2], (brickRect.x, brickRect.y))
    # Blitting brick debris
    for brick in breakingBrick:
        screen.blit(brickPiece[0], (brick[0] - brick[5], brick[1]))
        screen.blit(brickPiece[1], (brick[0] + 21 + brick[5], brick[1]))
        screen.blit(brickPiece[2], (brick[0] - brick[5] / 2, brick[1] + 21))
        screen.blit(brickPiece[3], (brick[0] + 21 + brick[5] / 2, brick[1] + 21))
    # Blitting coins
    for coin in coins:
        coinRect = coin[0], coin[1], coin[2], coin[3]
        screen.blit(coinsPic[0][int(spriteCount // 2)], coinRect)
    # Blitting bullet bills
    for bullet in bullets:
        bullRect = Rect(bullet[0], bullet[1], bullet[2], bullet[3])
        bullPic = enemiesPic[1][0]
        if bullet[BULLVX] > 0:
            bullPic = transform.flip(bullPic, True, False)
        screen.blit(bullPic, bullRect)
    # Blitting flag
    screen.blit(flagPic[0],(flagInfo[0][0],flagInfo[0][1]))
    screen.blit(flagPic[1],(flagInfo[1][0],flagInfo[1][1]))
    # Blitting mario
    marioShow = marioPic[marioFrame[0]][int(marioFrame[1])]
    if mario[DIR] == "Left":
        marioShow = transform.flip(marioShow, True, False)  # Flipping mario's sprite if he's facing left
    if marioStats[INVULFRAMES]%2 == 0 or marioStats[ISANIMATING]:
        screen.blit(marioShow, (mario[0], mario[1]))  # Blitting mario's sprite
    # Blitting floating points
    for point in points:
        pointText = marioFontThin.render("%s" %point[3], False, WHITE)
        screen.blit(pointText, (point[0], point[1]))
    # Blitting mute icon
    if isMuted:
        screen.blit(mutePic, (735,25))
    #for brick in brickList:
    #    draw.rect(screen,GREEN,(brick[0],brick[1],brick[2],brick[3]))


def moveBricks(questionBricks, interactBricks, breakingBrick):
    BRICKVY, IDLE, TYPE = 4, 5, 6
    for brick in questionBricks:
        if brick[BRICKVY] != 3.5 and brick[IDLE] == 1:
            brick[BRICKVY] += 0.5
            brick[1] += brick[BRICKVY]
    for brick in interactBricks:
        if brick[BRICKVY] != 3.5 and brick[IDLE] == 1:
            brick[BRICKVY] += 0.5
            brick[1] += brick[BRICKVY]
        else:
            brick[BRICKVY] = 0
            brick[IDLE] = 0
    for brick in breakingBrick:
        brick[1] += brick[4]
        brick[4] += 0.8
        brick[5] += 3


def floatObjects(moveCoins, points):
    X, Y, COINVY = 0, 1, 4
    PTSCOUNT, PTSNUM = 2, 3
    for coin in range(len(moveCoins) - 1, -1, -1):
        if moveCoins[coin][COINVY] != 5:
            moveCoins[coin][COINVY] += 0.5
            moveCoins[coin][Y] += moveCoins[coin][COINVY]
        else:
            points.append([moveCoins[coin][X], moveCoins[coin][Y], 30, 200])
            del moveCoins[coin]
    for point in range(len(points) - 1, -1, -1):
        points[point][PTSCOUNT] -= 1
        points[point][Y] -= 1


def moveItems(rectList, enemiesList, mushrooms, goombas, spinys):
    X, Y, DELAY, MOVEUP, MUSHVX, MUSHVY, INFLOOR = 0, 1, 4, 5, 6, 7, 8
    ENMYVX, ENMYVY, ENMYIDLE, ENMYINFLOOR = 4, 5, 6, 7
    # Making sure all mushrooms are activated
    for mushroom in mushrooms:
        if mushroom[DELAY] > 0:
            mushroom[DELAY] -= 1
        elif mushroom[MOVEUP] > 0:
            mushroom[MOVEUP] -= 1
            mushroom[1] -= 1
        else:
            itemCollide(mushroom, rectList, [X, Y, MUSHVX, MUSHVY, INFLOOR])
    for goomba in goombas:
        if goomba[ENMYIDLE] == 1:
            itemCollide(goomba, rectList, [X, Y, ENMYVX, ENMYVY, ENMYINFLOOR], enemiesList[:2])
        if goomba[ENMYIDLE] == 2:
            goomba[ENMYINFLOOR] -=1
    for spiny in spinys:
        if spiny[ENMYIDLE] == 1:
            itemCollide(spiny, rectList, [X, Y, ENMYVX, ENMYVY, ENMYINFLOOR], enemiesList[:2])


def itemCollide(item, rectList, indexList, extraCollideIn = None):
    X, Y, VX, VY, INFLOOR = indexList[0], indexList[1], indexList[2], indexList[3], indexList[4]
    ENMYVX, ENMYVY, ENMYIDLE, ENMYINFLOOR = 4, 5, 6, 7
    extraCollide = copy.deepcopy(extraCollideIn)
    if extraCollide != None:
        for list in range(len(extraCollide)):
            if item in extraCollide[list]:
                del extraCollide[list][extraCollide[list].index(item)]
        rectList = rectList + extraCollide
    item[X] += item[VX]
    item[VY] += 0.6
    item[Y] += item[VY]
    itemRect = Rect(item[0] + 3, item[1], item[2] - 3, item[3])
    if item[Y] > 496 and not item[INFLOOR]:
        item[Y] = 496
        item[VY] = 0
        try:
            if itemRect.x > 0 and screen.get_at((itemRect.x, itemRect.bottom)) == SKYBLUE and screen.get_at((itemRect.right, itemRect.bottom)) == SKYBLUE:
                item[INFLOOR] = True
        except IndexError:
            pass
    try:
        if item[INFLOOR] and screen.get_at((itemRect.x, itemRect.bottom)) != SKYBLUE and screen.get_at((itemRect.right, itemRect.bottom)) != SKYBLUE:
            item[INFLOOR] = False
    except IndexError:
        pass
    itemRect = Rect(item[0], item[1], item[2], item[3])
    for list in rectList:
        for brick in list:
            brickRect = Rect(brick[0], brick[1], brick[2], brick[3])
            if itemRect.colliderect(brickRect) and itemRect != brickRect:
                if int(item[Y]) < brickRect.y:
                    item[Y] = brickRect.y - 42
                    item[VY] = 0
                else:
                    try:
                        if brick[ENMYIDLE] != 2:
                            item[VX] *= -1
                    except IndexError:
                        item[VX] *= -1

def shootBullets(gunRects, bullets, mario):
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    GUNSTATE, GUNCOUNT, GUNTYPE = 4, 5, 6
    BULLVX, BULLVY = 4, 5
    for gun in gunRects:
        if gun[GUNTYPE] == 1 and gun[GUNSTATE] == 1:  # Checking if it's the gun or just cosmetic
            gun[GUNCOUNT] += 1
            if gun[GUNCOUNT] == 180:
                gun[GUNCOUNT] = 0
                bulletVX = -3
                xOffset = -48
                if mario[X] > gun[X]:
                    bulletVX = 3
                    xOffset = 42
                bullets.append([gun[X] + xOffset, gun[Y], 48, 42, bulletVX, 0])
                playSound(shootSound, "enemy")
    for bullet in bullets:
        if bullet[BULLVY] == 0:
            bullet[X] += bullet[BULLVX]
        else:
            bullet[BULLVY] += 0.6
            bullet[Y] += bullet[BULLVY]

def drawStats(mario, marioInfo, points, coins, startTime, level, fastMode, timesUp, coinPic, spriteCount, forceTime = None):
    ONGROUND, JUMPFRAMES, INGROUND, ISCROUCH, ONPLATFORM, ISFALLING, ISANIMATING, INVULFRAMES = 0, 1, 2, 3, 4, 5, 6, 7
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    nowFast = fastMode
    timesUpCheck = timesUp
    currentTime = 200 - int((time.get_ticks() - startTime) / 1000)
    if forceTime != None:
        currentTime = forceTime
    if currentTime < 100 and not fastMode and forceTime is None:
        playSound(timeLowSound, "music")
        playSound(backgroundFastSound, "music", True)
        nowFast = True
    if currentTime == 0 and not timesUp and forceTime is None:
        currentTime = 0
        marioInfo[ISANIMATING] = True
        mario[STATE] = -1
        timesUpCheck = True
    points = marioFontBig.render("%06i" %int(points), False, (255,255,255))
    coins =  marioFontBig.render("x%02i" %int(coins), False, (255,255,255))
    world = marioFontBig.render("1-%i" %int(level), False, (255,255,255))
    timer = marioFontBig.render("%03i" %int(currentTime), False, (255,255,255))
    screen.blit(points, (75,50))
    screen.blit(marioText, (75,25))
    screen.blit(coins, (300,50))
    screen.blit(worldText, (450,25))
    screen.blit(world, (470,50))
    screen.blit(timeText, (625,25))
    screen.blit(timer, (640, 50))
    screen.blit(coinPic[int(spriteCount//2)], (275,48))
    return nowFast, timesUpCheck

def drawPause():
    alphaSurface = Surface((800, 600))  # Making a surface
    alphaSurface.set_alpha(128)  # Giving it alpha functionality
    alphaSurface.fill((0, 0, 0))  # Fill the surface with a black background
    screen.blit(alphaSurface, (0, 0))  # Blit it into the actual screen
    # Blitting text
    screen.blit(pauseText, (345,290))
    screen.blit(helpText, (210, 330))

def moveSprites(mario, marioInfo, frame, forceTime = None):
    """ Function to cycle through Mario's sprites """
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    ONGROUND, JUMPFRAMES, INGROUND, ISCROUCH, ONPLATFORM, ISFALLING, ISANIMATING, INVULFRAMES = 0, 1, 2, 3, 4, 5, 6, 7
    changingSprites = [[2,5], [2,4], [2,5], [2,4], [2,5], [2,4], [1,0]]
    isDead = False
    if marioInfo[ISANIMATING]:
        if mario[STATE] == -1:
            forceTime = 0
            if frame[2] > 70:
                isDead = True
        if frame[2] == 55:
            marioInfo[ISANIMATING] = False
            frame[2] = 0
            if mario[STATE] == 0:
                mario[Y] += 42
                frame[0], frame[1] = 0, 0
            return isDead, forceTime
        if mario[STATE] == -1 and frame[2] == 0:  # If mario is dying, play his dying animation
            frame[0], frame[1] = 2, 3
            frame[2] = -15
            playSound(deathSound, "music")
        elif mario[STATE] == -1:
            frame[0], frame[1] = 2, 3
            frame[2] += 0.4
            if frame[2] > -9:
                mario[Y] += frame[2]
        elif mario[STATE] == 0:
            for index in range(len(changingSprites)):
                if changingSprites[index] == [2,5]:
                    changingSprites[index] = [1,0]
                elif changingSprites[index] == [1,0]:
                    changingSprites[index] = [2,5]
            frame[2] += 1
            frame[0], frame[1] = changingSprites[(frame[2]//8)][0], changingSprites[(frame[2]//8)][1]
        elif mario[STATE] == 1:
            frame[2] += 1
            frame[0], frame[1] = changingSprites[(frame[2]//8)][0], changingSprites[(frame[2]//8)][1]
        return isDead, forceTime
    if marioInfo[ONGROUND]:
        frame[0] = 0 + mario[STATE] # Adjusting for sprite for = big mario
        # Mario's running sprite counter
        if frame[1] < 3.8 and mario[VY] < 2:
            frame[1] += mario[VX]**2/100 + 0.2
        else:
            frame[1] = 1
        if frame[1] > 3.9:  # Sprite counter upper limit
            frame[1] = 3.9
        if mario[VX] == 0:  # If mario isn't moving, stay on his standing sprite
            frame[1] = 0
    else:
        frame[0],frame[1] = 2, 0 + mario[STATE]  # If mario is midair, stay on his jumping sprite
    if marioInfo[ISCROUCH]:
        frame[0],frame[1] = 2, 2  # If mario is crouching, stay on his crouching sprite
    if marioInfo[INVULFRAMES] != 0:
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
    try:
        if marioInfo[INGROUND] and screen.get_at((int(mario[X]+4),int(mario[Y]+marioOffset)))!=SKYBLUE and \
           screen.get_at((int(mario[X]+38),int(mario[Y]+marioOffset)))!=SKYBLUE: # Allow mario to recover if he goes back above the ground
            marioInfo[INGROUND] = False
    except:
        pass
    if marioInfo[INGROUND] and mario[Y] > 700:
        marioInfo[ISANIMATING] = True
        mario[STATE] = -1
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
    if marioRect.colliderect(poleRect):
        isPole = True
        mario[X] = poleRect.x - 16
        playSound(flagSound, "music")
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
    for index in range(len(breakingBrick) - 1, -1, -1):
        if breakingBrick[index][1] > 600:
            del breakingBrick[index]
    for list in range(len(itemsList)):
        for item in range(len(itemsList[list]) - 1, -1, -1):
            if itemsList[list][item][0] < -300 or itemsList[list][item][1] > 650:
                del itemsList[list][item]
    for list in range(len(rectList)):
        for rect in range(len(rectList[list]) - 1, -1, -1):
            if rectList[list][rect][0] < -700:
                del rectList[list][rect]
    for list in range(len(enemiesList)):
        for rect in range(len(enemiesList[list]) - 1, -1, -1):
            if enemiesList[list][rect][0] < -300 or enemiesList[list][rect][1] > 650:
                del enemiesList[list][rect]
    for point in range(len(points) - 1, -1, -1):
        if points[point][2] == 0:
            del points[point]
    # Activating and deactivating all enemies
    for list in range(len(enemiesList)):
        for enemy in range(len(enemiesList[list]) - 1, -1, -1):
            if enemiesList[list] == goombas or enemiesList[list] == spinys:
                # Activating goombas and spinys if they get close
                if enemiesList[list][enemy][ENMYIDLE] == 0 and enemiesList[list][enemy][X] < 800:
                    enemiesList[list][enemy][ENMYIDLE] = 1
                # Deleting them if they are crushed by mario
                elif enemiesList[list][enemy][ENMYIDLE] == 2 and enemiesList[list][enemy][ENMYINFLOOR] == 0:
                    points.append([enemiesList[list][enemy][0], enemiesList[list][enemy][1], 40, 100])
                    del enemiesList[list][enemy]
            elif enemiesList[list] == bullets:
                # Deleting bullets if they are too far off screen
                if enemiesList[list][enemy][0] < -1600 or enemiesList[list][enemy][0] > 1600:
                    del enemiesList[list][enemy]
    for gun in range(len(gunsList) - 1, -1, -1):
        # Activating guns if they get close and deleting them if they get too far back
        if gunsList[gun][0] < 1600:
            gunsList[gun][GUNSTATE] = 1
        if gunsList[gun][0] < -1600:
            del gunsList[gun]

def playSound(soundFile, soundChannel, queue = False):
    """ Function to load in sounds and play them on a channel """
    channelList = [["music", 0], ["effect", 1], ["block", 2], ["extra", 3], ["enemy", 4]]  # List to keep track of mixer channels
    for subList in channelList:  # For loop to identify the input
        if subList[0] == soundChannel:
            channelNumber = subList[1]
    if queue:
        mixer.Channel(channelNumber).queue(soundFile)  # Add the sound to the queue
    else:
        mixer.Channel(channelNumber).stop()  # Stopping any previous sound
        mixer.Channel(channelNumber).play(soundFile)  # Playing new sound

def globalSound(command):
    """ Function to apply commands to all mixer channels """
    for id in range(mixer.get_num_channels()):
        if command == "stop":
            mixer.Channel(id).stop()
        elif command == "pause":
            mixer.Channel(id).pause()
        elif command == "unpause":
            mixer.Channel(id).unpause()
        elif command == "toggleVol":
            if mixer.Channel(id).get_volume() == 0:
                mixer.Channel(id).set_volume(1)
            else:
                mixer.Channel(id).set_volume(0)


def spriteCounter(counter):
    """ Function to progress the universal sprite counter"""
    counter += 0.2
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
        line = line.strip("\n")  # Removing any line seperators
        line = line.split(",")  # Dividing elements seperated by commas
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
    pausedBool = False
    isMuted = False
    if mixer.Channel(0).get_volume() == 0:  # Checking current volume and fixing mute boolean accordingly
        isMuted = True
    timesUp = False
    isDead = False
    isPole = False
    isDone = False
    fast = False
    uniSprite = 0  # Counter to control all non - Mario sprites
    forceTime = None
    # Declaring session specific lists
    breakingBrick = []
    moveCoins = []
    mushrooms = []
    bullets = []
    points = []
    # Declaring packaged lists
    rectList = [brickList, interactBricks, questionBricks, gunRects]
    clearRectList = [coins, moveCoins, breakingBrick, mushrooms, goombas, points, flagInfo, bullets, spinys]
    itemsList = [mushrooms]
    enemiesList = [goombas, spinys, bullets]
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
                # TEMPORARY KEY INPUTS
                elif evnt.key == K_o:
                    if marioPos[STATE] == 0:
                        marioPos[STATE] = 1
                    else:
                        marioPos[STATE] = 0
                elif evnt.key == K_0:
                    marioPos = [0, 496, 0, 0, "Right", 0]
                    marioStats = [True, 0, False, False, False, False, False, 0]
                elif evnt.key == K_BACKSLASH:
                    return "loading"
                elif evnt.key == K_SLASH:
                    marioPos = [0, 496, 5, 0, "Right", 0]
                    while backPos > -15000:
                        walkMario(marioPos, rectList, "Right", clearRectList)
                elif evnt.key == K_PERIOD:
                    return "gameOver"
            elif evnt.type == KEYUP:
                # Keep track of when user lets go of space
                if evnt.key == K_SPACE:
                    marioStats[ISFALLING] = True
                # Keep track of when user lets go of the crouch key
                elif evnt.key== K_s:
                    marioStats[ISCROUCH]=False
            elif evnt.type == MOUSEBUTTONDOWN:
                RECTFINDER = [mx,my]
        # Functions to run during normal play
        if not pausedBool and not marioStats[ISANIMATING] and not isPole:
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
        if marioStats[ISANIMATING]:
            isDead, forceTime = moveSprites(marioPos, marioStats, marioFrame, forceTime)
        # Functions to run during Mario's end of level animation
        if isPole and not pausedBool:
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
        if isDead:
            levelNum -= 1
            marioScore[LIVES] -= 1
            if marioScore[LIVES] == 0:
                return "gameOver"
            return "loading"
        if isDone:
            if levelNum == 5:
                return "win"
            return "loading"
        print(RECTFINDER[0] - backPos, RECTFINDER[1], mx - RECTFINDER[0], my - RECTFINDER[1] )

def menu(selected):
    """ Function to reset all game variables and display the menu screen """
    global levelNum, marioScore
    # Resetting volume and game variables
    if mixer.Channel(0).get_volume() == 0:
        globalSound("toggleVol")
    levelNum = 4
    marioScore= [0, 0, 5]
    running = True
    globalSound("stop") # Stop any music that's playing
    # Menu screen variables
    textPoints = [[360, 350], [290, 390], [333, 430], [360, 470]]
    textList = [playText, instructText, creditText, quitText]
    returnList = ["loading", "instructions", "credit", "exit"]
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                return ["exit", None]
            if evnt.type == KEYDOWN:
                # Checking for menu screen inputs
                if evnt.key == K_UP or evnt.key == K_w:
                    selected -= 1
                elif evnt.key == K_DOWN or evnt.key == K_s:
                    selected += 1
                elif evnt.key == K_RETURN:
                    return [returnList[selected], selected]
        # Keeping the cursor within the bounds of the options
        if selected < 0:
            selected = 3
        elif selected > 3:
            selected = 0
        # Drawing the background and buttons
        screen.blit(backgroundPics[0],(0,0))
        screen.blit(marioSprites[0][0], (40, 496))
        screen.blit(titleLogo,(160,80))
        for index in range(len(textList)):
            screen.blit(textList[index], (textPoints[index][0], textPoints[index][1]))
        screen.blit(titleSelect, (textPoints[selected][0] - 30, textPoints[selected][1] - 4 ))
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
    # Loading screen variables
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
        screen.fill(BLACK)
        uniSprite = spriteCounter(uniSprite)
        drawStats(None, None, marioScore[PTS], marioScore[COIN], time.get_ticks(), levelNum, True, True, statCoin, uniSprite)
        screen.blit(currentWorld, (300, 250))
        screen.blit(lives, (390, 315))
        screen.blit(marioSprites[0][0], (315, 300))
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
        screen.blit(overText,(300,300))
        display.flip()
        fpsCounter.tick(60)
    return "menu"

def win(marioPos):
    """ Function to display winning screen"""
    PTS, COIN, LIVES = 0, 1, 2
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    globalSound("stop") # Stopping any music
    playSound(gameDoneSound, "music") # Playing win music
    if marioPos[STATE] == 0:
        marioPos = [-50, 495, 5, 0, "Right", 0]
    else:
        marioPos = [-50, 451, 5, 0, "Right", 1]
    frame = [0,0,0]
    canExit = False
    startTime = None
    running = True
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                return "exit"
            elif evnt.type == KEYDOWN:
                if evnt.key == K_RETURN and canExit:
                    return "menu"
        # Moving Mario
        if marioPos[X] < 350:
            marioPos[X] += 5
        elif startTime == None:
            startTime = time.get_ticks()
            marioPos[VX] = 0
        moveSprites(marioPos, marioStats, frame, 0)
        # Drawing win screen
        screen.fill(BLACK)
        screen.blit(winPics[0], (0, 0))
        screen.blit(winPics[1], (430, 467))
        screen.blit(marioSprites[frame[0]][int(frame[1])], (marioPos[X], marioPos[Y]))
        # Checking for text times and drawing text
        if startTime != None:
            timeDiff = time.get_ticks() - startTime
            screen.blit(winText1, (250,170))
            if timeDiff > 2000:
                screen.blit(winText2, (190, 260))
            if timeDiff > 4000:
                screen.blit(winText3, (160, 300))
            if timeDiff > 6000:
                screen.blit(winText4, (135, 390))
                canExit = True
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
        screen.blit(marioSprites[1][0],(130,450))
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
