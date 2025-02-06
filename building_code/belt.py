import time
from building_code.base import Building
class Belt(Building):
    def __init__(self,x,y,sides):
        super().__init__(x,y)

        self.outdirs=[]
        self.indirs=[]
        for x,side in enumerate(sides):
            if side=="in":
                self.indirs.append(x+1)
            elif side=="out":
                self.outdirs.append(x+1)

        self.currentchoice=0#for round robin purposes

        self.time=time.time()
        self.inv=[]
        self.maxinv=4
        self.complete=[]
        self.maxcomp=4
        self.type="belt"
    def tick(self,adjacents,speed=1):
        if time.time()-self.time>speed:
            self.time=time.time()
            self.craft()
        if len(self.complete)>0:
            try:
                vector={1:(0,-1),2:(-1,0),3:(0,1),4:(1,0)}
                opposite={1:3,2:4,3:1,4:2}
                chosendir=[]
                for dirs in self.outdirs:
                    if opposite[dirs] in adjacents[dirs].indirs:
                        chosendir.append(dirs)
                

                self.currentchoice+=1
                return vector[chosendir[self.currentchoice%len(chosendir)]]
            except:
                return False
        else:
            return False
    
    def craft(self):
        if len(self.inv)>0 and len(self.complete)<self.maxcomp:
            self.complete.append(self.inv.pop(0))
    
    def use(self,other):
        if len(other.inv)<other.maxinv:
            other.inv.append(self.complete.pop(0))
