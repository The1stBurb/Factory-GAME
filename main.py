import pygame,random,math
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
beltIn=pb.imgGit("img\\belts\\in.png",sz,sz)
beltOut=pb.imgGit("img\\belts\\out.png",sz,sz)
class belt:
    def __init__(self,x,y,up=False,right=False,down=False,left=False):
        print(up,right,down,left)
        self.img=self.buildImg(up,right,down,left)
        self.x,self.y=x,y
    def buildImg(self,up,right,down,left):
        if up==False and right==False and down==False and left==False:#not (up or right or down or left):
            return pb.imgGit("img\\belts\\belt_22.png",sz,sz)
        blankSrfce=pygame.Surface((sz,sz),pygame.SRCALPHA)
        for rot,i in enumerate([up,left,down,right]):
            if i==1:
                blankSrfce.blit(pb.rotate_image(beltIn,(rot-1)*90),(0,0))
            elif i==2:
                blankSrfce.blit(pb.rotate_image(beltOut,(rot-1)*90),(0,0))
        return blankSrfce
    def disp(self):
        screen.blit(self.img,(self.x*sz,self.y*sz))
belts=[]
class item:
    def __init__(self,location,name,price,idd):
        self.img=pb.imgGit(location,20,20)
        self.name=name
        self.price=price
        self.idd=idd
items=[item("img\\items\\RawCu.png","Raw Copper",0.50,0),item("img\\items\\RefinedCu.png","Refined Copper",1.50,1),]
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
        grid.append(["blank" for j in range(widh)])
#anything in that is "setup" goes here
def setup():
    buildGrid(50,50)
setup()
ms=[0,0]#mouse
grd=[0,0]#the offset made by panning the screen
pms=[0,0]#past mouse for dragging
drag=False
buttons=[False,False,False]
while True:
    screen.fill((200,200,200))
    # mbt=1
    pbtn=buttons
    buttons = pygame.mouse.get_pressed()
    keys=pygame.key.get_pressed()
    pms=ms.copy()
    ms=[pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]]
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            # print(clickclack)
            quit()
        elif i.type==pygame.KEYDOWN and i.key==pygame.K_RIGHT:
            pygame.mixer.music.stop()
    
    #this is drag
    if buttons[2]:
        grd=[grd[0]+(ms[0]-pms[0]),grd[1]+(ms[1]-pms[1])]
        drag=True
    elif drag:
        drag=False
    #set - unecesary
    elif buttons[0] and not pbtn[0]:
        rx=(ms[0]-grd[0])//sz
        ry=(ms[1]-grd[1])//sz
        grid[ry][rx]=f"belt{len(belts)}"
        # print(grid[ry][rx][:-1])
        belts.append(belt(rx,ry,1 if ry>0 and "belt"in grid[ry-1][rx] else 0,1 if rx<len(grid[ry])-1 and "belt"in grid[ry][rx+1] else 0,1 if ry<len(grid)-1 and "belt"in grid[ry+1][rx] else 0,1 if rx>0 and "belt"in grid[ry][rx-1] else 0,))
        for i in range(len(belts)):
            if math.sqrt((rx-belts[i].x)**2+(ry-belts[i].y)**2)<2:
                belts[i].img=belts[i].buildImg(1 if belts[i].y>0 and "belt"in grid[belts[i].y-1][belts[i].x] else 0,1 if belts[i].x<len(grid[belts[i].y])-1 and "belt"in grid[belts[i].y][belts[i].x+1] else 0,1 if belts[i].y<len(grid)-1 and "belt"in grid[belts[i].y+1][belts[i].x] else 0,1 if belts[i].x>0 and "belt"in grid[belts[i].y][belts[i].x-1] else 0,)
    for blt in belts:
        blt.disp()
    # #display grid
    # for y,i in enumerate(grid):
    #     for x,j in enumerate(i):
    #         pb.image(screen,imgs[j],x*sz+grd[0],y*sz+grd[1])
    pygame.display.flip()

    sfx.runAmb()
