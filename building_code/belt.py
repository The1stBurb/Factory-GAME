import time
from building_code.base import Building
class Belt(Building):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.time=time.time()
        self.inv=[]
        self.maxinv=4
        self.complete=[]
        self.maxcomp=4
        self.type="belt"

    def tick(self):
        if time.time()-self.time>1:
            self.time=time.time()
            self.craft()
        if len(self.complete)>0:
            return (1,0)
        else:
            return False
    
    def craft(self):
        if len(self.inv)>0 and len(self.complete)<self.maxcomp:
            self.complete.append(self.inv.pop(0))
    
    def use(self,other):
        if len(other.inv)<other.maxinv:
            other.inv.append(self.complete.pop(0))