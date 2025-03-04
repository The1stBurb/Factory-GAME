from save_code.comPile import runPiler
#this runs the whole save stuff, it smart
saveNum=2
def clearSave(saveOver=saveNum):
    runPiler(saveOver,"",encode=False)
def clearAll():
    for i in range(5):
        clearSave(i+1)