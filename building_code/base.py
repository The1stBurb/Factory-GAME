import time
#This is the parent class for buildings to inheret from, for ease of use
class Building:
    def __init__(self):
        self.time=time.time()#for crafting objects and making sure they take the correct amount of time
        # first slot in input, second is output
        self.inv=[None,None]
    
    def tick(self,speed):
        #speed is how often to "craft"
        if time.time()-self.time>speed:
            self.time=time.time()
            return True #we will then run the use function
   
    