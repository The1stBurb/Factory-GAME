import pygame,random
from keep import *
import pygameBases as pb
#comments should consist of, what does this do, why is it here, when is it used
pygame.init()
pygame.mixer.init()
X = 1000
Y = 1000
screen = pygame.display.set_mode((X, Y),pygame.RESIZABLE)#,pygame.FULLSCREEN)
clk=pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont(None, 10)
#runs SFX duh
class SFXRunner:
    def __init__(self):
        self.ambient=['sfx\\back1.wav','sfx\\back2.wav','sfx\\back3.wav','sfx\\back4.wav','sfx\\back5.wav','sfx\\back6.wav',]
        self.ambOn=random.randint(0,len(self.ambient)-1)
        # self.msOnClk=pygame.mixer.Sound('sound_file.wav')
        # self.msYes=pygame.mixer.Sound('sound_file.wav')
        # self.msNo=pygame.mixer.Sound('sound_file.wav')
    def runAmb(self):
        if not pygame.mixer.music.get_busy():
            self.ambOn=random.randint(0,len(self.ambient)-1)
            pygame.mixer.music.load(self.ambient[self.ambOn])
            pygame.mixer.music.play()
            print(self.ambient[self.ambOn])
sfx=SFXRunner()
#size of images
sz=100
#list of image for ease of use and stuff lol
imgs=[]#{"build":[],"belt":[],"icon":[],"item":[],"other":[]}
#raw for easy convert
rawImg={"building":["CuCond","FeCond","Sell"]}
#raw to img convert
for i in rawImg:
    for j in rawImg[i]:
        imgs.append(pb.imgGit(f"img\\{i}\\{j}.png",sz,sz),)
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
    keys=pygame.key.get_pressed()
    pms=ms.copy()
    ms=[pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]]
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            # print(clickclack)
            quit()
        elif i.type==pygame.KEYDOWN and i.key==pygame.K_RIGHT:
            pygame.mixer.music.stop()
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

    sfx.runAmb()
