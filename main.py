import pygame,random,math
from keep import *
import pygameBases as pb
from save_code.comPile import runPiler
from building_code.base import sz
import building_code.belt as belt
import building_code.building as build
#comments should consist of, what does this do, why is it here, when is it used
pygame.init()
pygame.mixer.init()
X = 1000
Y = 700
screen = pygame.display.set_mode((X, Y),pygame.RESIZABLE)#,pygame.FULLSCREEN)
clk=pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont(None, 10)
#for updating with upgrades
global moneyScaler
global cuCondScaler
global beltSpeedScaler
moneyScaler = 1
cuCondScaler = 1
beltSpeedScaler = 1
#runs SFX duh
class SFXRunner:
    def __init__(self):
        self.ambient=['sfx\\back1.wav','sfx\\back2.wav','sfx\\back3.wav','sfx\\back4.wav','sfx\\back5.wav','sfx\\back6.wav',]
        self.ambOn=random.randint(0,len(self.ambient)-1)
        # self.msOnClk=pygame.mixer.Sound('sound_file.wav')
        # self.msYes=pygame.mixer.Sound('sound_file.wav')
        # self.msNo=pygame.mixer.Sound('sound_file.wav')
        self.mute=True
    def runAmb(self):
        if not pygame.mixer.music.get_busy() and not self.mute:
            self.ambOn=random.randint(0,len(self.ambient)-1)
            pygame.mixer.music.load(self.ambient[self.ambOn])
            pygame.mixer.music.play()
            print(self.ambient[self.ambOn])
sfx=SFXRunner()
class item:
    def __init__(self,location,name,price,idd):
        self.img=pb.imgGit(location,20,20)
        self.name=name
        self.price=price
        self.idd=idd
#size of images
beltIn=pb.imgGit("img\\belts\\in.png",sz,sz)
beltOut=pb.imgGit("img\\belts\\out.png",sz,sz)
beltIn=pb.imgGit("img\\belts\\in.png",sz,sz)
beltOut=pb.imgGit("img\\belts\\out.png",sz,sz)
items=[item("img\\items\\RawCu.png","Raw Copper",0.50,0),item("img\\items\\RefinedCu.png","Refined Copper",1.50,1),]
#list of image for ease of use and stuff lol
imgs={}#{"build":[],"belt":[],"icon":[],"item":[],"other":[]}
#raw for easy convert
rawImg={"building":["CuCond","FeCond","Sell"]}
#raw to img convert
for i in rawImg:
    for j in rawImg[i]:
        imgs[j]=pb.imgGit(f"img\\{i}\\{j}.png",sz,sz)
#grid of blocks
grid=[]
#self explanitory
def buildGrid(width,high):
    global grid
    for i in range(width):
        grid.append([0 for j in range(width)])
#anything in that is "setup" goes here
def setup():
    buildGrid(50,50)
#Checks all the buildings
def tick(buildings):
    pass
    for building in buildings:
        if isInstance(building,belt.Belt):
            building.tick(beltSpeedScaler)
        elif isInstance(building,build.CuCond):
            building.tick(cuCondScaler)
setup()
ms=[0,0]#mouse
grd=[0,0]#the offset made by panning the screen
pms=[0,0]#past mouse for dragging
drag=False
buttons=[False,False,False]
types=0
up,right,down,left=pygame.K_UP,pygame.K_RIGHT,pygame.K_DOWN,pygame.K_LEFT
n1,n2,n3,n4,n5,n6,n7,n8,n9,n0=pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9,pygame.K_0
place=1#False
toPlace=[]
def main():
    global grid,ms,grd,pms,drag,buttons,types,up,right,down,left,n1,n2,n3,n4,n5,n6,n7,n8,n9,n0,place,toPlace
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
                print(toPlace)
                quit()
            elif i.type==pygame.KEYDOWN and i.key==pygame.K_RIGHT:
                pygame.mixer.music.stop()
        if keys[n0]:
            types=0
        elif keys[n1]:
            types=1
        #this is drag
        if buttons[2]:
            grd=[grd[0]+(ms[0]-pms[0]),grd[1]+(ms[1]-pms[1])]
            drag=True
        elif drag:
            drag=False
        elif buttons[0] and not pbtn[0]:
            if place==False:
                rx=(ms[0]-grd[0])//sz
                ry=(ms[1]-grd[1])//sz
                # grid[ry][rx]=f"belt{len(belts)}"
                if types==0:
                    grid[ry][rx]=belt.Belt(rx,ry)
                elif types==1:
                    grid[ry][rx]=build.CuCond(rx,ry,imgs["CuCond"])
                grid[ry][rx].buildImg(grid,beltIn,beltOut)
                if ry>0 and grid[ry-1][rx]!=0:
                    grid[ry-1][rx].buildImg(grid,beltIn,beltOut)
                if ry<len(grid)-1 and grid[ry+1][rx]!=0:
                    grid[ry+1][rx].buildImg(grid,beltIn,beltOut)
                if rx>0 and grid[ry][rx-1]!=0:
                    grid[ry][rx-1].buildImg(grid,beltIn,beltOut)
                if rx<len(grid[ry])-1 and grid[ry][rx+1]!=0:
                    grid[ry][rx+1].buildImg(grid,beltIn,beltOut)
        if place==1:
            rx=(ms[0]-grd[0])//sz
            ry=(ms[1]-grd[1])//sz
            prx=(pms[0]-grd[0])//sz
            pry=(pms[1]-grd[1])//sz
            if [rx,ry]!=[prx,pry] and [rx,ry]in toPlace and toPlace.index([rx,ry])==len(toPlace)-2:
                toPlace.remove([rx,ry])
            elif [rx,ry]!=[prx,pry]and math.sqrt((prx-rx)**2+(pry-ry)**2)<2:
                toPlace.append([rx,ry])
                # print(rx,ry,math.sqrt((prx-rx)**2+(pry-ry)**2))
        for y,i in enumerate(grid):
            for x,j in enumerate(i):
                pb.rect(screen,x*sz+grd[0],y*sz+grd[1],sz,sz,width=2)
                if j!=0:
                    pb.image(screen,j.disp,j.x*sz+grd[0],j.y*sz+grd[1]-(j.disp.get_height()-sz))
                # pb.image(screen,imgs[j],x*sz+grd[0],y*sz+grd[1])
        for i in toPlace[:-1]:
            pb.rect(screen,i[0]*sz+grd[0],i[1]*sz+grd[0],sz,sz,col=(0,0,0))
        pygame.display.flip()
        sfx.runAmb()
titleBtn=pb.imgGit("img\\other\\title_screen\\title.png",730,110)
creditBtn=pb.imgGit("img\\other\\title_screen\\credits.png",380,90)
startBtn=pb.imgGit("img\\other\\title_screen\\start.png",300,90)
savesBtn=pb.imgGit("img\\other\\title_screen\\saves.png",290,90)
def start():
    while True:
        width=pygame.display.get_surface().get_width()
        screen.fill((200,200,200))
        svx,svy=(width-savesBtn.get_width())/2,savesBtn.get_height()*2.5+startBtn.get_height()*1.5+titleBtn.get_height()
        stx,sty=(width-startBtn.get_width())/2,startBtn.get_height()*1.5+titleBtn.get_height()
        ttx,tty=(width-titleBtn.get_width())/2,titleBtn.get_height()/2
        cdx,cdy=(width-creditBtn.get_width())/2,creditBtn.get_height()*1.5+savesBtn.get_height()*2.5+startBtn.get_height()*1.5+titleBtn.get_height()
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                # print(clickclack)
                quit()
            elif i.type==pygame.MOUSEBUTTONDOWN:
                mx,my=pygame.mouse.get_pos()
                if mx>=stx and mx<=stx+startBtn.get_width() and my>=sty and my<=sty+startBtn.get_height():
                    return "start"
                elif mx>=cdx and mx<=cdx+creditBtn.get_width() and my>=cdy and my<=cdy+creditBtn.get_height():
                    return "credits"
                elif mx>=svx and mx<=svx+savesBtn.get_width() and my>=svy and my<=svy+savesBtn.get_height():
                    return "saves"
        screen.blit(titleBtn,(ttx,tty))
        screen.blit(startBtn,(stx,sty))
        screen.blit(savesBtn,(svx,svy))
        screen.blit(creditBtn,(cdx,cdy))
        pygame.display.flip()
        
while True:
    action="start"#start()
    match action:
        case "start":
            main()
        case "credits":
            pass
        case "saves":
            pass
