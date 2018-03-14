import os
import json as js

PATH_TO_DATA = "../Data"

Total = 0
Categorized = 0
for dir in os.listdir(PATH_TO_DATA):
    Total+=1
    with open(os.path.join(PATH_TO_DATA,dir,"document.json"),"r") as f:
        doc_json = js.load(f)
        if len(doc_json["Categories"])!=0:
            Categorized +=1
        if len(doc_json["Categories"])>1:
            print("find")

print(Categorized/Total)