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

page = "credit"
fpsCounter = time.Clock()
marioPos = [0, 0, 0, True] # X, Y, VY, ONGROUND
backgroundPics = [image.load("assets\\backgrounds\\level_"+str(i)+".png") for i in range(1,1)]
marioSprites = []
marioState = 0 # 0 is small, 1 is big mario
levelNum = 0 # Using 0 as level 1 since indexes start at 0

# Declaring Rects

#smallMario = Rect()
    
# Loading Pictures
    
for i in range (1,1):
    backgroundPics.append(image.load("assets\\backgrounds\\level_"+str(i)+".png"))
    

# Declaring game functions


# Declaring main functions

def game():
    pass

def menu():
    pass

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
        page = simpleGame()    
    if page == "instructions":
        page = instructions()     
    if page == "credit":
        page = credit()  
    

quit()
