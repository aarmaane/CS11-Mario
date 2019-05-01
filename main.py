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

# Declaring variables

fpsCounter = time.Clock()
menu = "game"
marioPos = [0, 0, 0, 0]

# Declaring Rects

smallMario = Rect (


# Declaring main functions

def game():
    pass

def menu():
    pass

def loading():
        '''running = True
    loading = image.load(".png")
    loading = transform.smoothscale(story, screen.get_size())
    screen.blit(story,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False
        display.flip()
    return "menu"  '''                           

def instructions():
        '''running = True
    loading = image.load(".png")
    loading = transform.smoothscale(story, screen.get_size())
    screen.blit(story,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False
        display.flip()
    return "menu"  '''   
        
def credit():
        '''running = True
    loading = image.load(".png")
    loading = transform.smoothscale(story, screen.get_size())
    screen.blit(story,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False
        display.flip()
    return "menu"  '''      

running = True
while running:
    for evt in event.get():
        if evt.type == QUIT:
            running = False

    mb = mouse.get_pressed()
    mx, my = mouse.get_pos()
    display.flip()
    
page = "menu"
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
