import pygame,random,math,os,save,pygameBases as pyb,building_code.belt as belt, building_code.building as build
from save_code.comPile import runPiler
from building_code.base import sz
#comments should consist of, what does this do, why is it here, when is it used
pygame.init()
pygame.mixer.init()
X = 1100
Y = 700
screen = pygame.display.set_mode((X, Y),pygame.RESIZABLE)#,pygame.FULLSCREEN)
pb=pyb.pb(screen)
clk=pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont(None, 10)
#for updating with upgrades
# global moneyScaler
# global cuCondScaler
# global beltSpeedScaler
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
    def widthy(self,msgs,width,sz,iters=0):
        # return msgs
        if iters>100:return msgs
        msgs2=[]
        rebuilt=False
        for i in msgs:
            for digi in range(len(i)):
                if digi*round(sz*7)>width:
                    closest=min(width//round(sz*7)+1,len(i)-1)
                    closest=i.rfind(" ",0,closest)
                    if closest==-1:break
                    msgs2.append(i[:closest])
                    msgs2.append(" "+i[closest+1:])
                    rebuilt=True
                    break
            else: msgs2.append(i)
        if rebuilt: return self.widthy(msgs2,width,sz,iters+1)
        return msgs2
    def print(self,msgs,x,y,colour=lightpurple,sz=0,shadow=False,width=10**10000,right_align=False):
        sz=self.sz if sz==0 else sz
        msgs=self.widthy(str(msgs).split("\n"),width,sz)
        for yps,msg in enumerate(msgs):
            if right_align==True:pb.translate(-math.ceil(len(msg)*sz*6),0)
            for xps,i in enumerate(msg):
                if shadow==True:
                    # pb.image(pb.resize(self.ltr[i.lower()],sz*6,sz*7),x+xps*6*sz,y-1*sz+yps*6*sz)
                    pb.image(pb.resize(pb.recolour(self.ltr[i.lower()],colour),sz*6,sz*7),x-sz+math.ceil(xps*6*sz),y+math.ceil(yps*6*sz))
                else:
                    pb.image(pb.resize(pb.recolour(self.ltr[i.lower()],colour),sz*6,sz*7),x-sz+math.ceil(xps*6*sz),y+math.ceil(yps*6*sz))
            if right_align==True:pb.pop()
text=Text(10)
class ResearchTree:
    def __init__(self,sz,loadImgs=True):
        self.grey=self.green=self.prple={}
        self.rpoints={"Base":0,"BetterPower":0,"EvenBetterPower":0,"Fluids":0,"Overclock":0,"Ads":0,"SuperAds":0,"AdvancedBase":0,"AdvancedOilProcess":0,"AdvancedWire":0,"BrainWashing":0,"Circuit2":0,"Circuit3":0,"Circuit4":0,"Circuit5":0,"Circuit6":0,"Circuit7":0,"Circuit8":0,"Circuit8.5":0,"Circuit9":0,"Circuit10":0,"CircuitInfinity":0,"CircuitReligion":0,"CompressedCrystal":0,"Crystal":0,"EliteBase":0,"EliteWire":0,"EndGame":0,"ExpandFactory":0,"FracturedPower":0,"ImprovedResearch":0,"IndustrialPower":0,"Logistics1":0,"Logistics2":0,"Logistics3":0,"MagicPower":0,"MoreMines":0,"NuclearPower":0,"NuclearResearch":0,"Oil&Plastic":0,"RealityCrystal":0,"RealityMines":0,"Rods":0,"StockTrading":0,"Teleporters":0,"TimeWarp":0,"UltimateBase":0,"UltimateWire":0,}
        self.texts={"Base":"Everyone starts somewhere!",'BetterPower': 'Its normal Power, but Better!', 'EvenBetterPower': 'Its normal Power, but Even Better!', 'Fluids': 'You discover how to use and move Oil and Water!', 'Overclock': 'Make it run faster but not quite so faster that it goes boom!', 'Ads': 'Make advertisements so more people buy your stuff, which means more money!', 'SuperAds': 'Its normal Ads, but Super!', 'AdvancedBase': "It's a normal base, but Advanced!", 'AdvancedOilProcess': 'Process your Oil, but Advancedly!', 'AdvancedWire': 'Its normal wire, but Advanced!', 'BrainWashing': 'Make the people Want your products, instead of just Needing them!', 'Circuit2': 'A normal Circuit, but 2x better!', 'Circuit3': 'A normal Circuit, but 3x better!', 'Circuit4': 'A normal Circuit, but 4x better!', 'Circuit5': 'A normal Circuit, but 5x better!', 'Circuit6': 'A normal Circuit, but 6x better!', 'Circuit7': 'A normal Circuit, but 7x better!', 'Circuit8': 'A normal Circuit, but 8x better!', "Circuit8.5":"A normal Circuit, but 8.5x better!",'Circuit9': 'A normal Circuit, but 9x better!', 'Circuit10': 'A normal Circuit, but 10x better!', 'CircuitInfinity': 'A normal Circuit, but Infinity times better!', 'CircuitReligion': 'Start a Religion based around Circuits, to get people to buy more!', 'CompressedCrystal': 'More Crystal per Crystal!', 'Crystal': 'You find some shiny rocks...', 'EliteBase': 'The Elite version of a Base!', 'EliteWire': 'The Elite version of Wires!', 'EndGame': 'It, just like, ends the game. Whats so hard to understand?', 'ExpandFactory': 'You can buy more land, to build more Factory!', 'FracturedPower': 'Its Power, but Fractured. Nobody knows how it works.', 'ImprovedResearch': 'Make your researchers Research more better!', 'IndustrialPower': 'Pollute that environment! Who cares, anyways?', 'Logistics1': 'Make things run more better!', 'Logistics2': 'Make things run even more better!', 'Logistics3': 'Make things run even more betterer!', 'MagicPower': "It's magically magical!", 'MoreMines': 'You can make more mines!', 'NuclearPower': 'You discover how to split the atom!', 'NuclearResearch': 'Can we smash atoms together, instead of apart? Who knows!', 'Oil&Plastic': 'Oil can make this cool rock, we should name it Plastic!', 'RealityCrystal': 'Mine Reality to get these Crystals!', 'RealityMines': 'Mine Reality itself!', 'Rods': 'Why not? They are good weapons!', 'StockTrading': 'Manipulate the Stock Market, so people buy your stuff!', 'Teleporters': 'Make things move even faster!', 'TimeWarp': 'Make your factory enter a different time stream, so it runs faster!', 'UltimateBase': 'The Ultimate version of a Base!', 'UltimateWire': 'The Ultimate version of Wires!'}
        self.spots={'[45,277]':'BetterPower','[160,277]':'EvenBetterPower','[110,384]':'Fluids','[464,182]':'Overclock','[376,540]':'Ads','[515,539]':'SuperAds','[0,277]':'Base','[324,384]':'AdvancedOilProcess','[677,445]':'AdvancedWire',"[243,329]":"AdvancedBase",'[827,542]':'BrainWashing','[50,58]':'Circuit2','[118,58]':'Circuit3','[200,58]':'Circuit4','[270,58]':'Circuit5','[338,57]':'Circuit6','[428,57]':'Circuit7','[506,57]':'Circuit8','[599,57]':'Circuit8.5','[700,57]':'Circuit9',"[803,57]":"Circuit10",'[915,56]':'CircuitInfinity',"[704,542]":"CircuitReligion",'[975,56]':'EndGame','[590,384]':'CompressedCrystal','[457,383]':'Crystal','[398,330]':'EliteBase','[795,444]':'EliteWire','[148,3]':'ExpandFactory','[889,286]':'FracturedPower','[42,492]':'ImprovedResearch','[352,278]':'IndustrialPower','[107,129]':'Logistics1','[208,129]':'Logistics2','[300,130]':'Logistics3','[700,280]':'MagicPower','[236,445]':'MoreMines','[536,280]':'NuclearPower','[234,490]':'NuclearResearch','[198,384]':'Oil&Plastic','[730,385]':'RealityCrystal','[543,441]':'RealityMines','[97,220]':'Rods','[910,129]':'StockTrading','[777,130]':'Teleporters','[630,168]':'TimeWarp','[616,331]':'UltimateBase','[917,445]':'UltimateWire'}
        self.highlight=""
        self.research,self.bought,self.needs=[],[],["BetterPower","EvenBetterPower","Fluids","Overclock","Ads","SuperAds","AdvancedBase","AdvancedOilProcess","AdvancedWire","BrainWashing","Circuit2","Circuit3","Circuit4","Circuit5","Circuit6","Circuit7","Circuit8","Circuit8.5","Circuit9","Circuit10","CircuitInfinity","CircuitReligion","CompressedCrystal","Crystal","EliteBase","EliteWire","EndGame","ExpandFactory","FracturedPower","ImprovedResearch","IndustrialPower","Logistics1","Logistics2","Logistics3","MagicPower","MoreMines","NuclearPower","NuclearResearch","Oil&Plastic","RealityCrystal","RealityMines","Rods","StockTrading","Teleporters","TimeWarp","UltimateBase","UltimateWire",]
        if loadImgs:
            tot=len(os.listdir("img/research_tree"))
            self.base_grey,self.base_green,self.base_prple=pb.imgGit("img/research_tree/bases/grey.png",24*sz,24*sz),pb.imgGit("img/research_tree/bases/green.png",24*sz,24*sz),pb.imgGit("img/research_tree/bases/prple.png",24*sz,24*sz)
            for i,fils in enumerate(os.listdir("img/research_tree")):
                if os.path.isdir(f"img\\research_tree\\{fils}"):continue
                screen.fill((255,255,255))
                text.print(f"{i}/{tot-1} Research Tree Imgs loaded",0,0,sz=5)
                text.print("|"+("&"*(i+1))+(" "*(tot-(i+1)))+"|",0,25,sz=2)
                pb.flip()
                nfils=fils.replace(".png","")
                if nfils in self.research: self.prple[nfils]=pb.imgGit(f"img\\research_tree\\{fils}",1000*sz,580*sz)
                elif nfils in self.bought: self.green[nfils]=pb.imgGit(f"img\\research_tree\\{fils}",1000*sz,580*sz)
                elif nfils in self.needs: self.grey[nfils]=pb.imgGit(f"img\\research_tree\\{fils}",1000*sz,580*sz)
            _btn=pb.imgGit("img\\research_tree\\bases\\yes-no.png",36,11)
            _sz=2
            self.yes=pb.resize(_btn.subsurface((0,0,21,11)),_sz*21,_sz*11)
            self.no=pb.resize(_btn.subsurface((22,0,14,11)),_sz*14,_sz*11)
    def disp(self):
        for i in self.spots:
            spot=eval(i)
            nam=self.spots[i]
            if nam in self.grey:pb.image(self.base_grey,spot[0],spot[1])
            elif nam in self.green:pb.image(self.base_green,spot[0],spot[1])
            elif nam in self.prple:pb.image(self.base_prple,spot[0],spot[1])
        for img in self.needs:
            pb.image(self.grey[img],0,0)
        for img in self.research:
            pb.image(self.transp[img],0,0)
        for img in self.bought:
            pb.image(self.norm[img],0,0)
        if self.highlight!="":
            pb.rect(0,0,X,Y,col=(100,100,100,200))
            if self.highlight in self.grey:
                pb.image(self.grey[self.highlight])
            elif self.highlight in self.transp:
                pb.image(self.transp[self.highlight])
            elif self.highlight in self.norm:
                pb.image(self.norm[self.highlight])
rt=ResearchTree(1,False)
class item:
    def __init__(self,location,name,price,idd):
        self.img=pb.imgGit(location,20,20)
        self.name=name
        self.price=price
        self.idd=idd
#size of images
error=pb.imgGit("img\\error.png",sz,sz)
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
def setup(sz):
    buildGrid(sz,sz)
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
        pb.flip()

#All the SAVEable variables
grid=[]
moneyScaler = 1
cuCondScaler = 1
beltSpeedScaler = 1
money=0
#none more after this pls, will make saving 36.5 times as easy
def saveStuff(encode=True):
    #variables here
    global grid,moneyScaler,cuCondScaler,beltSpeedScaler,money
    #classes here
    global rt
    saveList=(grid,moneyScaler,cuCondScaler,beltSpeedScaler,money,"Seperator! Yay!",rt.needs,rt.bought,rt.research)
    runPiler(save.saveNum,str(saveList),encode=encode)
def unSaveStuff():
    #variables here
    global grid,moneyScaler,cuCondScaler,beltSpeedScaler,money
    #classes here
    global rt
    saved=runPiler(save.saveNum)
    if saved=="":
        saveStuff()
        print("Started new save!")
    else:
        grid,moneyScaler,cuCondScaler,beltSpeedScaler,money,_,rt.needs,rt.bought,rt.research=eval(saved)
    # print(grid)
setup(10)

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
def box(mx,my,x,y,w=24,h=24):
    return mx>=x and my>=y and mx<=x+w and my<=y+h
def runResearchTree():
    pastbtn,buttons=[False,False,False],[0,0,0]
    while True:
        screen.fill((200,200,200))
        # buttons = pygame.mouse.get_pressed()
        ms=[pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]]
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                # print(toPlace)
                return
            elif i.type==pygame.MOUSEBUTTONDOWN:
                if i.button==1:
                    print(pygame.mouse.get_pos())
                    buttons[0]=True
            # elif i.type==pygame.MOUSEBUTTONUP:
            #     buttons=[False,False,False]
        rt.disp()
        if rt.highlight!="":
            pb.rect(X-340,-10,340,50,radius=15,col=lightpurple)
            text.print(f"1.23K/1.23K Research Points",X-5,0,colour=(0,0,0),sz=2,right_align=True)
            # pb.image(rt.yes,X-300,30)
        for i in rt.spots:
            if box(ms[0],ms[1],eval(i)[0],eval(i)[1]):
                pb.translate((X-110 if ms[0]+110>X else ms[0])+(10 if ms[1]-50<0 else 0),(ms[1] if ms[1]-50<0 else ms[1]-50))#
                pb.rect(0,0,111,51,col=(50,50,50))
                pb.rect(0,0,110,50,col=(100,100,100))
                pb.rect(0,8,110,42,col=(120,120,120))
                text.print(rt.spots[i],1,1,sz=1)
                text.print(rt.texts[rt.spots[i]],1.5,9,colour=(255,255,255),sz=1,width=110)
                text.print(f"1.23K/1.23K Research Points",2,37,colour=(255,255,255),sz=0.86,width=111)
                if not rt.highlight in["",rt.spots[i]]:
                    pb.rect(0,0,111,51,col=(0,0,0,200))
                pb.pop()
                if buttons[0]and not pastbtn[0]:
                    buttons[0]=False
                    # print(rt.highlight)
                    rt.highlight=rt.spots[i] if rt.highlight!=rt.spots[i] else ""
                    # print(rt.highlight)
        pb.flip()
        pastBtn=buttons.copy()
        # buttons=[False,False,False]
unSaveStuff()
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
            print("Saving...")
            saveStuff(encode=True)
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
            pb.rect(x*sz+grd[0],y*sz+grd[1],sz,sz,width=2)
            if j!=0:
                pb.image(j.image,j.x*sz+grd[0],j.y*sz+grd[1])
            # pb.image(imgs[j],x*sz+grd[0],y*sz+grd[1])
    # text.print("ABCDEFghijklmnopqrstuvwxyz`1234567890-=[]\\;',./~!@#$%^&*()_+{}|:\"<>? ",0,0,shadow=True)
    pb.flip()
    sfx.runAmb()
