import time

class CuCond:
    def __init__(self,x,y,baseImg):
        self.x=x
        self.y=y
        self.image=baseImg
        self.time=time.time()
        self.outdirs=[1,2,3,4]
        self.indirs=[]
        self.inv=[]
        self.maxinv=0
        self.complete=[]
        self.maxcomp=4
        self.type="building"

    def tick(self,speed=1):
        if time.time()-self.time>speed:
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
#base class to copy
# class Belt(Building):
#     def __init__(self,x,y):
#         super().__init__(x,y)
#         self.time=time.time()
#         self.inv=[]
#         self.maxinv=
#         self.complete=[]
#         self.maxcomp=
#         self.type="building"

#     def tick(self,speed=1):
#         if time.time()-self.time>speed:
#             self.time=time.time()
#             self.craft()
#         if len(self.complete)>0:
#             return (1,0)
#         else:
#             return False
    
#     def craft(self):
#         if len(self.inv)>0 and len(self.complete)<self.maxcomp:
#             self.complete.append(self.inv.pop(0))
    
#     def use(self,other):
#         if len(other.inv)<other.maxinv:
#             other.inv.append(self.complete.pop(0))
