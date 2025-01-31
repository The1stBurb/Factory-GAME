#this is a class thats only purpose is to keep track of things that have an x/y
class xANDy:
    def __init__(self):
        self.x=0
        self.y=0
    def setVal(self,pnts):
        self.x=pnts[0]
        self.y=pnts[1]
    def git(self):
        return self.x,self.y
