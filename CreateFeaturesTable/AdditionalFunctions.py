import re
from functools import reduce

def DeleteSpacesAndNewLineSigns(s):
    string = re.sub("\n+"," ",s)
    string = re.sub("\s(\s+)"," ", string)
    string = re.sub("^\s+", "", string)
    string = re.sub("\s+$", "", string)
    return string

def RemovePunctuation(s):
    string = re.sub("\s\W"," ",s)
    string = re.sub("\W\s"," ",string)
    string = re.sub("\s\W\s", " ", string)
    string = re.sub("_", " ", string)
    return string

def FixIncorrectWordsAndTokenize(listString):
    russianWordPattern = re.compile(r"^[а-я]+$")
    numberPattern = re.compile(r"^[0-9]+$")
    listS = reduce(lambda list,x: list + [x] if (russianWordPattern.match(x)!=None) else (list + ['number'] if (numberPattern.match(x)!=None) else list), listString, [])
    return listS


