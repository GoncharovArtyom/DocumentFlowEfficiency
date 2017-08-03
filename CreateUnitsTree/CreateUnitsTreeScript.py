import jpath as jp
import os as os
import json as js
import Organization
import Unit
from MyEncoder import MyEncoder
from AdditionalFunctons import *

path = r"C:\Users\Артем\Documents\Диплом\Данные\data"
listDir = os.listdir(path)
organization = Organization.Organization()

for i in range(len(listDir)):
    print(i)
    curDir = listDir[i]
    curPath = path + "\\" + curDir 
    f = open(curPath + "\\resolution.json" ,'r')
    obj = js.load(f)
    f.close()
    AddUnitsFromResolutionObj(obj, organization)

organization.SaveToJson(r"C:\Users\Артем\Documents\Диплом\DocumentFlowEffeciency\DocumentFlowEffeciency\org1.json")
    
    



        



