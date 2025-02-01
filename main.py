import pygame,random
from keep import *
import pygameBases as pb
#comments should consist of, what does this do, why is it here, when is it used
pygame.init()
X = 1000
Y = 1000
screen = pygame.display.set_mode((X, Y),pygame.RESIZABLE)#,pygame.FULLSCREEN)
clk=pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont(None, 10)
#this is for ease of use terms of pygame displaying stuff
    

#size of images
sz=100
#list of image for ease of use and stuff lol
imgs=[
    pb.imgGit("img\\blank.png",sz,sz),pb.imgGit("img\\refiner-1.png",sz,sz),
]
#grid of blocks
grid=[]
#self explanitory
def buildGrid(widh,high):
    global grid
    for i in range(widh):
        grid.append([0 for j in range(widh)])
#anything in that is "setup" goes here
def setup():
    buildGrid(50,50)
setup()
ms=[0,0]#mouse
grd=[0,0]#the offset made by panning the screen
pms=[0,0]#past mouse for dragging
drag=False
while True:
    screen.fill((200,200,200))
    # mbt=1
    pms=ms.copy()
    ms=[pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]]
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            # print(clickclack)
            quit()
    buttons = pygame.mouse.get_pressed()
    #this is drag
    if buttons[2]:
        grd=[grd[0]+(ms[0]-pms[0]),grd[1]+(ms[1]-pms[1])]
        drag=True
    elif drag:
        drag=False
    #set - unecesary
    elif buttons[0]:
        rx=(ms[0]-grd[0])//sz
        ry=(ms[1]-grd[1])//sz
        grid[ry][rx]=1
    #display grid
    for y,i in enumerate(grid):
        for x,j in enumerate(i):
            pb.image(screen,imgs[j],x*sz+grd[0],y*sz+grd[1])
    pygame.display.flip()
