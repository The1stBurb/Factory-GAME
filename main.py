import pygame,random
from keep import *
#comments should consist of, what does this do, why is it here, when is it used
pygame.init()
X = 1000
Y = 1000
scrn = pygame.display.set_mode((X, Y),pygame.RESIZABLE)#,pygame.FULLSCREEN)
clk=pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont(None, 10)
#this is for ease of use terms of pygame displaying stuff
class pygameBases:
    def __init__(self):
        pass
    #re color an image
    def colorize(self,image, new_color):
        tinted = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        tinted.fill(new_color)
        tinted.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return tinted
    #resize an image
    def resize(self,img,w,h):
        return pygame.transform.scale(img,(w,h))
    #rotate an image
    def rot90(self,img,r=-1):
        if r==-1:
            r=random.randint(0,3)*90
        return pygame.transform.rotate(img,r)
    #create a rectanngle
    def rect(self,x,y,w,h,col=(255,255,255)):
        # print(col)
        pygame.draw.rect(scrn, col, pygame.Rect(x, y, w, h))
    #write text
    def text(self,txt,x,y,col=(0,0,0)):
        scrn.blit(font.render(txt, True, col),(x,y))
    #make a quadrilateral
    def quad(self,x1,y1,x2,y2,x3,y3,x4,y4,col=(255,255,255)):
        pygame.draw.polygon(scrn, col, [(x1,y1),(x2,y2),(x3,y3),(x4,y4),])
    #blit an image
    def image(self,img,x,y):
        scrn.blit(img,(x,y))
    #pull image form path
    def gitImg(self,path):
        return pygame.image.load(path).convert_alpha()
    #pull image and resize lol
    def imgGit(self,path,w,h):
        return self.resize(self.gitImg(path),w,h)
pb=pygameBases()
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
ms=xANDy()#mouse
grd=xANDy()#grid x and y
pms=xANDy()#past mouse for dragging
drag=False
while True:
    scrn.fill((200,200,200))
    # mbt=1
    pms.setVal(ms.git())
    ms.setVal(pygame.mouse.get_pos())
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            # print(clickclack)
            quit()
    buttons = pygame.mouse.get_pressed()
    #this is drag
    if buttons[2]:
        grd.setVal((grd.x+(ms.x-pms.x),grd.y+(ms.y-pms.y)))
        drag=True
    elif drag:
        drag=False
    #set - unecesary
    elif buttons[0]:
        rx=ms.x//sz
        ry=ms.y//sz
        grid[ry][rx]=1
    #display grid
    for y,i in enumerate(grid):
        for x,j in enumerate(i):
            pb.image(imgs[j],x*sz+grd.x,y*sz+grd.y)
    pygame.display.flip()
