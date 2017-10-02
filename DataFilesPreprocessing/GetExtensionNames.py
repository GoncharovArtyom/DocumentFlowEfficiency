
import os
import re

path = r"/home/artyom/Документы/dms"
dirs = os.listdir(path)
a = set()
for dir in dirs:
    files = os.listdir(path+"/"+dir)
    for file in files:
        tmp = file.split('.')
        if (tmp[len(tmp) - 1] == "pdf"):
            print(dir)
        a.add(tmp[len(tmp) - 1])

print(a)
