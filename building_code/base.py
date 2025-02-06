import time
import pygameBases as pb
import pygame
sz=100
#This is the parent class for buildings to inheret from, for ease of use
class Building:
    def __init__(self,x,y):
        self.x,self.y=x,y
        self.beltSides=[False,False,False,False]
        self.time=time.time()#for crafting objects and making sure they take the correct amount of time
        # first slot in input, second is output
        self.inv=[None,None]
        self.img=None#pygame.Surface((sz,sz),pygame.SRCALPHA)
    
    def tick(self,speed):
        #speed is how often to "craft"
        if time.time()-self.time>speed:
            self.time=time.time()
            return True #we will then run the use function
    def buildImg(self,grid,beltIn,beltOut):
        up=right=down=left=False
        if self.y>0 and grid[self.y-1][self.x]!=0:
            up=1
        if self.y<len(grid)-1 and grid[self.y+1][self.x]!=0:
            down=1
        if self.x>0 and grid[self.y][self.x-1]!=0:
            left=1
        if self.x<len(grid[self.y])-1 and grid[self.y][self.x+1]!=0:
            right=1
        blankSrfce=pygame.Surface((sz,sz),pygame.SRCALPHA)
        if self.img!=None:
            blankSrfce.blit(self.img,(0,0))
        for rot,i in enumerate([up,left,down,right]):
            if i==1:
                blankSrfce.blit(pb.rotate_image(beltIn,(rot-1)*90),(-1 if rot==2 else 0,-1 if rot==1 else 0))
            elif i==2:
                blankSrfce.blit(pb.rotate_image(beltOut,(rot-1)*90),(-1 if rot==2 else 0,-1 if rot==1 else 0))
        self.beltSides=[up,right,down,left]
        self.img=blankSrfce
