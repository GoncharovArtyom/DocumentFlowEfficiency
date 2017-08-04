import os as os
import json as js
import Organization
import Unit
from MyEncoder import MyEncoder
from AdditionalFunctons import *

path = r"../data"
listDir = os.listdir(path)
organization = Organization.Organization()

for i in range(len(listDir)):
    print(i)
    curDir = listDir[i]
    curPath = os.path.join(path, curDir)
    f = open(os.path.join(curPath, "resolution.json"), 'r')
    obj = js.load(f)
    f.close()
    AddUnitsFromResolutionObj(obj, organization)

organization.SaveToJson(os.path.join(os.curdir,"organization.json"))
    
    



        



