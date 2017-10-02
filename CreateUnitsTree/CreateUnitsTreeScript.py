import os as os
import json as js
import Organization
import Unit
from MyEncoder import MyEncoder
from AdditionalFunctions import *

path = r"../dms"
listDir = os.listdir(path)
organization = Organization.Organization()

for i in range(len(listDir)):
    print(i)
    curDir = listDir[i]
    curPath = os.path.join(path, curDir)
    f = open(os.path.join(curPath, "resolution.json"), 'r')
    obj = js.load(f)
    f.close()
    AddUnitsFromResolutionObj(obj, organization, curDir)

organization.SaveToJson(os.path.join(r"../Files","dd_organization.json"))

    
    



        



