import pygame,random,math
from keep import *
import pygameBases as pb
from save_code.comPile import runPiler
from building_code.base import sz
import building_code.belt as belt
import building_code.building as build
import os
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
purple=(33,32,51)
darkpurple=(26,26,41)
lightpurple=(56,55,72)
class Text:
    def __init__(self,sz):
        self.ltr={}
        self.sz=sz
        ltrs=pb.imgGit("txtFiles\\text1.png",63,64)
        for x,i in enumerate("abcdefghijklmnopqrstuvwxyz`1234567890[]\\;',./~!@#$%^&*()_+{}|:\"<>? -="):
            # print(((x%9),(x//9)),i)
            self.ltr[i]=ltrs.subsurface(((x%9)*7,(x//9)*8,6,7))#((x%9)*(sz*7),(x-(x//9))*(sz*8),6*sz,7*sz))
    def print(self,msgs,x,y,colour=lightpurple,sz=0,shadow=False,width=10**100):
        msgs=str(msgs).split("\n")
        sz=self.sz if sz==0 else sz
        # msgs2=[]
        # for i in msgs:
        #     if len(msg)*sz>width:
        #         msgs2.append(i[:(width//sz)])
        #         msgs2.append(i[])
        #     else:
        #         msgs2.append(i)
        # print(msgs)
        for yps,msg in enumerate(msgs):
            for xps,i in enumerate(msg):
                if shadow==True:
                    # pb.image(screen,pb.resize(self.ltr[i.lower()],sz*6,sz*7),x+xps*6*sz,y-1*sz+yps*6*sz)
                    pb.image(screen,pb.resize(pb.recolour(self.ltr[i.lower()],colour),sz*6,sz*7),x-1*sz+xps*6*sz,y-1*sz+yps*6*sz)
                else:
                    pb.image(screen,pb.resize(pb.recolour(self.ltr[i.lower()],colour),sz*6,sz*7),(x-1+xps*6)*sz,y-1*sz+yps*6*sz)
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
#DONT KILL THIS HWILE JUST COMMNET OUT PLS
def box(mx,my,x,y,w=24,h=24):
    return mx>=x and my>=y and mx<=x+w and my<=y+h
researched=["BetterPower"]
bought=["EvenBetterPower"]
class ResearchTree:
    def __init__(self,sz):
        self.needs={}
        self.research={}
        self.bought={}
        self.texts={'Better Power': 'Its normal Power, but Better!', 'Even Better Power': 'Its normal Power, but Even Better!', 'Fluids': 'You discover how to use and move Oil and Water!', 'Overclock': 'Make it run faster but not quite so faster that it goes boom!', 'Ads': 'Make advertisements so more people buy your stuff, which means more money!', 'Super Ads': 'Its normal Ads, but Super!', 'Advanced Base': "It's a normal base, but Advanced!", 'Advanced Oil Process': 'Process your Oil, but Advancedly!', 'Advanced Wire': 'Its normal wire, but Advanced!', 'BrainWashing': 'Make the people Want your products, instead of just Needing them!', 'Circuit2': 'A normal Circuit, but 2x better!', 'Circuit3': 'A normal Circuit, but 3x better!', 'Circuit4': 'A normal Circuit, but 4x better!', 'Circuit5': 'A normal Circuit, but 5x better!', 'Circuit6': 'A normal Circuit, but 6x better!', 'Circuit7': 'A normal Circuit, but 7x better!', 'Circuit8': 'A normal Circuit, but 8x better!', 'Circuit9': 'A normal Circuit, but 9x better!', 'Circuit10': 'A normal Circuit, but 10x better!', 'CircuitInfinity': 'A normal Circuit, but Infinity times better!', 'CircuitReligion': 'Start a Religion based around Circuits, to get people to buy more!', 'CompressedCrystal': 'More Crystal per Crystal!', 'Crystal': 'You find some shiny rocks...', 'EliteBase': 'The Elite version of a Base!', 'EliteWire': 'The Elite version of Wires!', 'EndGame': 'It, just like, ends the game. Whats so hard to understand?', 'ExpandFactory': 'You can buy more land, to build more Factory!', 'FracturedPower': 'Its Power, but Fractured. Nobody knows how it works.', 'ImprovedResearch': 'Make your researchers Research more better!', 'IndustrialPower': 'Pollute that environment! Who cares, anyways?', 'Logistics1': 'Make things run more better!', 'Logistics2': 'Make things run even more better!', 'Logistics3': 'Make things run even more betterer!', 'MagicPower': "It's magically magical!", 'MoreMines': 'You can make more mines!', 'NuclearPower': 'You discover how to split the atom!', 'NuclearResearch': 'Can we smash atoms together, instead of apart? Who knows!', 'Oil&Plastic': 'Oil can make this cool rock, we should name it Plastic!', 'RealityCrystal': 'Mine Reality to get these Crystals!', 'RealityMines': 'Mine Reality itself!', 'Rods': 'Why not? They are good weapons!', 'StockTrading': 'Manipulate the Stock Market, so people buy your stuff!', 'Teleporters': 'Make things move even faster!', 'TimeWarp': 'Make your factory enter a different time stream, so it runs faster!', 'UltimateBase': 'The Ultimate version of a Base!', 'UltimateWire': 'The Ultimate version of Wires!'}
        self.spots={'[45,277]':'BetterPower','[160,277]':'EvenBetterPower','[110,384]':'Fluids','[464,182]':'Overclock','[376,540]':'Ads','[515,539]':'SuperAds','[0,277]':'Base','[324,384]':'AdvancedOilProcess','[677,445]':'AdvancedWire','[827,542]':'BrainWashing','[50,58]':'Circuit2','[118,58]':'Circuit3','[200,58]':'Circuit4','[270,58]':'Circuit5','[338,57]':'Circuit6','[428,57]':'Circuit7','[506,57]':'Circuit8','[599,57]':'Circuit8.5','[700,57]':'Circuit9',"[803,57]":"Circuit10",'[915,56]':'CircuitInfinity',"[704,542]":"CircuitReligion",'[975,56]':'EndGame','[590,384]':'CompressedCrystal','[457,383]':'Crystal','[398,330]':'EliteBase','[795,444]':'EliteWire','[148,3]':'ExpandFactory','[889,286]':'FracturedPower','[42,492]':'ImprovedResearch','[352,278]':'IndustrialPower','[107,129]':'Logistics1','[208,129]':'Logistics2','[300,130]':'Logistics3','[700,280]':'MagicPower','[236,445]':'MoreMines','[536,280]':'NuclearPower','[234,490]':'NuclearResearch','[198,384]':'Oil&Plastic','[730,385]':'RealityCrystal','[543,441]':'RealityMines','[97,220]':'Rods','[910,129]':'StockTrading','[777,130]':'Teleporters','[630,168]':'TimeWarp','[616,331]':'UltimateBase','[917,445]':'UltimateWire'}
        self.highlight=""
        tot=len(os.listdir("img/research_tree"))
        for i,fils in enumerate(os.listdir("img/research_tree")):
            screen.fill((255,255,255))
            text.print(f"{i}/{tot-1} Research Tree Imgs loaded",0,0,sz=5)
            text.print("|"+("&"*(i+1))+(" "*(tot-(i+1)))+"|",0,25,sz=2)
            pygame.display.flip()
            if fils in researched:
                self.research[fils]=pb.imgGit(f"img\\research_tree\\{fils}",1000*sz,580*sz)#pb.transparent()
            elif fils in bought:
                self.bought[fils]=pb.imgGit(f"img\\research_tree\\{fils}",1000*sz,580*sz)
            else:
                self.needs[fils]=pb.imgGit(f"img\\research_tree\\{fils}",1000*sz,580*sz)#pb.greyscale()
    def disp(self):
        for img in self.needs:
            pb.image(screen,self.needs[img],0,0)
        for img in self.research:
            pb.image(screen,self.research[img],0,0)
        for img in self.bought:
            pb.image(screen,self.bought[img],0,0)
rt=ResearchTree(1)
# its=iter(rt.texts)
# chos=next(its)
# print(chos)
while True:
    screen.fill((200,200,200))
    buttons = pygame.mouse.get_pressed()
    ms=[pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]]
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            print(toPlace)
            quit()
        # elif i.type==pygame.MOUSEBUTTONDOWN and i.button==1:
            # print(pygame.mouse.get_pos())
            # with open("research tree texts.txt","a")as rtt:
            #     rtt.write(f"\"{chos}\":{ms}")
            # chos=next(its)
            # print(chos)
    rt.disp()
    #circuit8.5,9,10,base
    # text.print(str(ms),0,20)
    for i in rt.spots:
        if box(ms[0],ms[1],eval(i)[0],eval(i)[1]):
            text.print(rt.spots[i],0,0)
            if pygame.mouse.get_pressed()[0]:
                rt.highlight=rt.spots[i]
    # if str(ms)in rt.spots:
    #     text.print(rt.spots[str(ms)],0,0)
    pygame.display.flip()
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
