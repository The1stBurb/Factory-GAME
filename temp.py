sq={"Better Power":[45, 277],"Even Better Power":[160, 277],"Fluids":[110, 384],"Overclock":[464, 182],"Ads":[376, 540],"Super Ads":[515, 539],"Advanced Base":[0, 277],"Advanced Oil Process":[324, 384],"Advanced Wire":[677, 445],"BrainWashing":[827, 542],"Circuit2":[50, 58],"Circuit3":[118, 58],"Circuit4":[200, 58],"Circuit5":[270, 58],"Circuit6":[338, 57],"Circuit7":[428, 57],"Circuit8":[506, 57],"Circuit9":[599, 57],"Circuit10":[700, 57],"CircuitInfinity":[915, 56],"CircuitReligion":[975, 56],"CompressedCrystal":[590, 384],"Crystal":[457, 383],"EliteBase":[398, 330],"EliteWire":[795, 444],"EndGame":[975, 56],"ExpandFactory":[148, 3],"FracturedPower":[889, 286],"ImprovedResearch":[42, 492],"IndustrialPower":[352, 278],"Logistics1":[107, 129],"Logistics2":[208, 129],"Logistics3":[300, 130],"MagicPower":[700, 280],"MoreMines":[236, 445],"NuclearPower":[536, 280],"NuclearResearch":[234, 490],"Oil&Plastic":[198, 384],"RealityCrystal":[730, 385],"RealityMines":[543, 441],"Rods":[97, 220],"StockTrading":[910, 129],"Teleporters":[777, 130],"TimeWarp":[630, 168],"UltimateBase":[616, 331],"UltimateWire":[917, 445],}
for i in sq:
    with open("temp.txt","a")as tt:
        tt.write(f"\"{i}\":0,")