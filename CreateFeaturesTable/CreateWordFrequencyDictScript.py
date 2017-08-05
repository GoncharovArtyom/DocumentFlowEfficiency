import pandas
import Stemmer
import os
import re
from CreateFeaturesTable.AdditionalFunctions import *
from WordCountDict import *

stemmer = Stemmer.Stemmer("russian")

pathTodata = "../data"
listDir = os.listdir(pathTodata)
filePattern = re.compile(".*.txt$")
wordCountDict = WordCountDict()
error = []
k=0

for i in range(len(listDir)):
    path = os.path.join(pathTodata,listDir[i])
    listFiles = os.listdir(path)
    for j in range(len(listFiles)):
        result = re.match(filePattern, listFiles[j])
        if (result != None):
            try:
                f = open(os.path.join(path,result.string), 'r')
                s = f.read()
                f.close()
                s = DeleteSpacesAndNewLineSigns(s)
                s = RemovePunctuation(s)
                s = s.lower()
                listString = s.split(" ")
                listString = FixIncorrectWordsAndTokenize(listString)
                listString = stemmer.stemWords(listString)
                wordCountDict.AddOrIncList(listString)
                print(k)
                k = k+1
            except UnicodeDecodeError:
                error.append((listDir[i], listFiles[j]))


print("k = ", k)
wordCountDict.Save(os.path.join(os.path.curdir,"dict.pkl"))
print(error)


