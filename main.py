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
class Text:
    def __init__(self,sz):
        self.ltr={}
        self.sz=sz
        ltrs=pb.imgGit("txtFiles\\text1.png",63,64)
        for x,i in enumerate("abcdefghijklmnopqrstuvwxyz`1234567890[]\\;',./~!@#$%^&*()_+{}|:\"<>? -="):
            # print(((x%9),(x//9)),i)
            self.ltr[i]=ltrs.subsurface(((x%9)*7,(x//9)*8,6,7))#((x%9)*(sz*7),(x-(x//9))*(sz*8),6*sz,7*sz))
    def print(self,msgs,x,y,sz=0,shadow=False):
        msgs=msgs.split("\n")
        # print(msgs)
        sz=self.sz if sz==0 else sz
        for yps,msg in enumerate(msgs):
            for xps,i in enumerate(msg):
                if shadow==True:
                    # pb.image(screen,pb.resize(self.ltr[i.lower()],sz*6,sz*7),x+xps*6*sz,y-1*sz+yps*6*sz)
                    pb.image(screen,pb.resize(self.ltr[i.lower()],sz*6,sz*7),x-1*sz+xps*6*sz,y-1*sz+yps*6*sz)
                else:
                    pb.image(screen,pb.resize(self.ltr[i.lower()],sz*6,sz*7),x-1*sz+xps*6*sz,y-1*sz+yps*6*sz)
text=Text(10)
class item:
    def __init__(self,location,name,price,idd):
        self.img=pb.imgGit(location,20,20)
        self.name=name
        self.price=price
        self.idd=idd
#size of images
error=pb.imgGit("img\\error.png",sz,sz)
beltIn=pb.imgGit("img\\belts\\in.png",sz,sz)
beltOut=pb.imgGit("img\\belts\\out.png",sz,sz)
beltIn=pb.imgGit("img\\belts\\in.png",sz,sz)
beltOut=pb.imgGit("img\\belts\\out.png",sz,sz)
items=[item("img\\items\\RawCu.png","Raw Copper",0.50,0),item("img\\items\\RefinedCu.png","Refined Copper",1.50,1),]
#at first glance this may seem ineffecient, but we have to load each image anyway
beltimgs={(None,"out",None,"in"):pb.imgGit("img\\belts\\belth11.png",sz,sz),
          (None,"in",None,"out"):pygame.transform.flip(pb.imgGit("img\\belts\\belth11.png",sz,sz),True,False),
          ("out",None,"in",None):pb.imgGit("img\\belts\\beltv11.png",sz,sz),
          ("in",None,"out",None):pygame.transform.flip(pb.imgGit("img\\belts\\beltv11.png",sz,sz),False,True),

          ("in","out",None,None):pygame.transform.flip(pb.imgGit("img\\belts\\beltcv11.png",sz,sz),False,True),
          (None,"out","in",None):pygame.transform.flip(pb.imgGit("img\\belts\\beltcv11.png",sz,sz),False,False),
          (None,None,"in","out"):pygame.transform.flip(pb.imgGit("img\\belts\\beltcv11.png",sz,sz),True,False),
          ("out",None,None,"in"):pygame.transform.flip(pb.imgGit("img\\belts\\beltch11.png",sz,sz),True,True),
          ("out","in",None,None):pygame.transform.flip(pb.imgGit("img\\belts\\beltch11.png",sz,sz),False,True),
          (None,"in","out",None):pygame.transform.flip(pb.imgGit("img\\belts\\beltch11.png",sz,sz),False,False),
          (None,None,"out","in"):pygame.transform.flip(pb.imgGit("img\\belts\\beltch11.png",sz,sz),True,False),
          ("in",None,None,"out"):pygame.transform.flip(pb.imgGit("img\\belts\\beltcv11.png",sz,sz),True,True),

          ("out","in",None,"in"):pygame.transform.rotate(pb.imgGit("img\\belts\\beltt21.png",sz,sz),90),
          (None,"in","out","in"):pygame.transform.rotate(pb.imgGit("img\\belts\\beltt21.png",sz,sz),270),
          ("in","out","in",None):pygame.transform.rotate(pb.imgGit("img\\belts\\beltt21.png",sz,sz),0),
          ("in",None,"in","out"):pygame.transform.rotate(pb.imgGit("img\\belts\\beltt21.png",sz,sz),180),

          ("out","in","in",None):pygame.transform.rotate(pb.imgGit("img\\belts\\beltl21.png",sz,sz),90),
          ("in",None,"out","in"):pygame.transform.rotate(pb.imgGit("img\\belts\\beltl21.png",sz,sz),270),
          (None,"out","in","in"):pygame.transform.rotate(pb.imgGit("img\\belts\\beltl21.png",sz,sz),0),
          ("in","in",None,"out"):pygame.transform.rotate(pb.imgGit("img\\belts\\beltl21.png",sz,sz),180),
          
          ("out","in","in",None):pygame.transform.rotate(pb.imgGit("img\\belts\\beltl21.png",sz,sz),90),
          ("in",None,"out","in"):pygame.transform.rotate(pb.imgGit("img\\belts\\beltl21.png",sz,sz),270),
          (None,"out","in","in"):pygame.transform.rotate(pb.imgGit("img\\belts\\beltl21.png",sz,sz),0),
          ("in","in",None,"out"):pygame.transform.rotate(pb.imgGit("img\\belts\\beltl21.png",sz,sz),180),
          
          ("out",None,"in","in"):pygame.transform.rotate(pygame.transform.flip(pb.imgGit("img\\belts\\beltl21.png",sz,sz),False,True),90),
          ("in","in","out",None):pygame.transform.rotate(pygame.transform.flip(pb.imgGit("img\\belts\\beltl21.png",sz,sz),False,True),270),
          ("in","out",None,"in"):pygame.transform.rotate(pygame.transform.flip(pb.imgGit("img\\belts\\beltl21.png",sz,sz),False,True),0),
          (None,"in","in","out"):pygame.transform.rotate(pygame.transform.flip(pb.imgGit("img\\belts\\beltl21.png",sz,sz),False,True),180),
          
          ("out","in","in","in"):pygame.transform.rotate(pb.imgGit("img\\belts\\belt31.png",sz,sz),90),
          ("in","in","out","in"):pygame.transform.rotate(pb.imgGit("img\\belts\\belt31.png",sz,sz),270),
          ("in","out","in","in"):pygame.transform.rotate(pb.imgGit("img\\belts\\belt31.png",sz,sz),0),
          ("in","in","in","out"):pygame.transform.rotate(pb.imgGit("img\\belts\\belt31.png",sz,sz),180),}
#list of image for ease of use and stuff lol
imgs={}#{"build":[],"belt":[],"icon":[],"item":[],"other":[]}
#raw for easy convert
rawImg={"building":["CuCond","FeCond","Sell"]}
#raw to img convert
for i in rawImg:
    for j in rawImg[i]:
        imgs[j]=pb.imgGit(f"img\\{i}\\{j}.png",sz,sz)
#grid of blocks

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
        if isinstance(building,build.CuCond):
            building.tick(cuCondScaler)
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



grid=[]
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
rotion=1#rotation used for placing buildings

keydown=False#to prevent double key presses for holding a key
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
    elif keys[pygame.K_r]:
        if not keydown:
            rotion+=1
            if rotion>4:rotion=1
        keydown=True
    else:
        keydown=False
    #this is drag
    if buttons[2]:
        grd=[grd[0]+(ms[0]-pms[0]),grd[1]+(ms[1]-pms[1])]
        drag=True
    elif drag:
        drag=False
    elif buttons[0]:
        
        rx=(ms[0]-grd[0])//sz
        ry=(ms[1]-grd[1])//sz
        # grid[ry][rx]=f"belt{len(belts)}"
        if types==0:
            sides=[None,None,None,None]
            opposite={1:3,2:4,3:1,4:2}
            for sidenum,side in enumerate(((0,-1),(1,0),(0,1),(-1,0))):
                square=grid[ry+side[1]][rx+side[0]]
                if not isinstance(square,int):
                    if opposite[sidenum+1] in square.outdirs:
                        sides[sidenum]="in"
                    elif sidenum==opposite[rotion]-1 and square.type=="belt" and not sidenum+1 in square.outdirs:
                        square.outdirs.append(sidenum+1)
                        square.refresh_image(beltimgs,error)
            sides[rotion-1]="out"
            if not "in" in sides:
                sides[opposite[rotion]-1]="in"
            try:
                grid[ry][rx]=belt.Belt(rx,ry,sides,beltimgs[tuple(sides)])
            except:
                grid[ry][rx]=belt.Belt(rx,ry,sides,error)
        elif types==1:
            grid[ry][rx]=build.CuCond(rx,ry,imgs["CuCond"])
        
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
                pb.image(screen,j.image,j.x*sz+grd[0],j.y*sz+grd[1])
            # pb.image(screen,imgs[j],x*sz+grd[0],y*sz+grd[1])
    text.print("ABCDEFghijklmnopqrstuvwxyz`1234567890-=[]\\;',./~!@#$%^&*()_+{}|:\"<>? ",0,0,shadow=True)
    pygame.display.flip()
    sfx.runAmb()
