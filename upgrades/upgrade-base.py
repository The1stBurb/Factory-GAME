class items:
    def __init__(self,needs,name,cost,unlocked):
        self.need=needs
        self.cost=cost
        self.name=name
        self.ulock=unlocked
    def __str__(self):
        return str(self.need)
    def buildable(self,built):
        ok=[""]
        for i in built:
            if i in self.need:
                ok.append("yay")
        if len(ok)!=len(self.need):
            return False
        else:
            return True
item=[
items([],"CuOre",0,True),
items(["CuOre"],"Cu",0,False),
items(["Cu"],"CuPlate",0,False),
items(["Cu"],"CuRod",0,False),

items(["CuPlate"],"Wire",0,False),
items(["LightOil","CuPlate"],"AdvWire",0,False),
items(["HeavyOil","CuPlate"],"UltWire",0,False),

items([],"FeOre",0,True),
items(["FeOre"],"Fe",0,False),
items(["Fe"],"FePlate",0,False),
items(["Fe"],"FeRod",0,False),

items(["FePlate"],"CircuitBase",0,False),
items(["FePlate","Plastic"],"AdvBase",0,False),
items(["FeRod","ActCrystal","EliteBase"],"UltBase",0,False),
items(["FeRod","CuRod","CircuitI"],"EliteBase",0,False),

items(["Wire","CircuitBase"],"CircuitI",0,False),
items(["Wire","CircuitBase"],"CircuitII",0,False),
items(["Wire","AdvBase"],"CircuitIII",0,False),
items(["CircuitIII","Plastic","Wire"],"CircuitIV",0,False),
items(["EliteBase","AdvWire"],"CircuitV",0,False),
items([""],"CircuitVI",0,False),
items([""],"CircuitVII",0,False),
items([""],"CircuitVIII",0,False),
items([""],"CircuitIX",0,False),
items([""],"CircuitX",0,False),
items([""],"Circuit8",0,False),

items([],"Oil",0,True),
items(["Oil"],"HeavyOil",0,False),
items(["Oil"],"LightOil",0,False),
items(["Oil","H2O"],"Plastic",0,False),

items([],"RawCrystal",0,True),
items(["RawCrystal","H2O"],"Crystal",0,False),
items(["Crystal","HeavyOil"],"ActCrystal",0,False),
items(["Crystal"],"CrystalDust",0,False),
items(["ActCrystal","CrystalDust"],"CompCrystal",0,False),
items(["CompCrystal","HeavyOil","LightOil"],"ActCompCrystal",0,False),
items(["CompCrystal"],"CompCrystalDust",0,False),
items(["ActCompCrystal","CompCrystalDust"],"RealityCrystal",0,False),
items(["RealityCrystal"],"RealityAshes",0,False),

items([],"H2O",0,True),
items([""],"Fluids",0,False),
]


#variables for basic unlocks:
# copperOreUnlocked = False
# refinedCopperUnlocked = False
# copperPlateUnlocked = False
# copperRodUnlocked = False
# wiresUnlocked = False
# advancedWiresUnlocked = False
# eliteWiresUnlocked = False
# rawCrystalUnlocked = False
# crystalUnlocked = False
# activatedCrystalUnlocked = False
# crystalDustUnlocked = False
# oilUnlocked = False
# heavyOilUnlocked = False
# lightOilUnlocked = False
# plasticUnlocked = False
# waterUnlocked = False
# ironOreUnlocked = False
# refinedIronUnlocked = False
# ironPlateUnlocked = False
# ironRodUnlocked = False

#variables for mid unlocks:
# compressedCrystalUnlocked = False
# activatedCompressedCrystalUnlocked = False
crystalMoldUnlocked = False
# advancedBaseUnlocked = False
# eliteBaseUnlocked = False
# circuitBaseUnlocked = False
# ultimateBaseUnlocked = False

#variables for high unlocks:
# compressedCrystalDustUnlocked = False
# realityCrystalUnlocked = False
# realityAshesUnlocked = False
# ultimateWiresUnlocked = False

#circuit unlocks:
# circuit1Unlocked = False
circuit1_5Unlocked = False
# circuit2Unlocked = False
circuit2_5Unlocked = False
# circuit3Unlocked = False
# circuit4Unlocked = False
# circuit5Unlocked = False
circuit5_5Unlocked = False
# circuit6Unlocked = False
# circuit7Unlocked = False
# circuit8Unlocked = False
circuit8_5Unlocked = False
# circuit9Unlocked = False
# circuit10Unlocked = False
# circuitloopingUnlocked = False
highestCircuitLoopUnlocked = 10

#even more endgame items:
reallyBigUpgradeThatEndsTheGameUnlocked = False
logistics1Unlocked = False
logistics2Unlocked = False
logistics3Unlocked = False
teleportersUnlocked = False

#upgrades:
betterPowerUnlocked = False
evenBetterPowerUnlocked = False
americaPowerUnlocked = False
nuclearPowerUnlocked = False
magicPowerUnlocked = False
fracturedPowerUnlocked = False
improvedResearchUnlocked = False
nuclearResearchUnlocked = False
timeWarpUnlocked = False
advertisingUnlocked = False
superAdvertisingUnlocked = False
circuitBasedReligionUnlocked = False
brainwashingUnlocked = False
stockTradingUnlocked = False
# fluidsUnlocked = False
expandableFactoryUnlocked = False
advancedOilProcessingUnlocked = False
moreMinesUnlocked = False
rodsUnlocked = False
